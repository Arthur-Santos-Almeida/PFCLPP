#include "ilcplex\cplex.h"
#include "ilcplex\ilocplex.h"

#include "gurobi_c++.h"

#include <iostream>
#include <chrono>

#define NOME_INSTANCIA "h2_w32_58_all"

#define DIRETORIO_MODELO "../../Model/"
#define DIRETORIO_SOLUCAO_CPLEX "../../Solution/Cplex/"
#define DIRETORIO_SOLUCAO_GUROBI "../../Solution/Gurobi/"
#define CPLEX_PREFIXO "cplex_"
#define GUROBI_PREFIXO "gurobi_"
#define LP ".lp"
#define SOL ".sol"

#define LIMITE_TEMPO 3600 // 1 hora

int cplex() {

    IloEnv env;
    IloModel model(env);
    IloCplex cplex(env);

    // Path de leitura
    const char* path = DIRETORIO_MODELO NOME_INSTANCIA LP;

    // Arrays para variáveis e restrições
    IloObjective obj(env);
    IloNumVarArray vars(env);
    IloRangeArray constraints(env);

    // Lê o modelo do .lp
    cplex.importModel(model, path, obj, vars, constraints);

    if (vars.getSize() == 0 && constraints.getSize() == 0) {
        std::cerr << "Erro: o arquivo " << path << " nao contem um modelo valido." << std::endl;
        return 1;
    }

    cplex.extract(model);

    // Define o limite de tempo
    cplex.setParam(IloCplex::Param::TimeLimit, LIMITE_TEMPO);

    // Inicia o cronômetro
    auto inicio = std::chrono::high_resolution_clock::now();

    // Resolve o .lp
    if (cplex.solve()) {
        // Finaliza o cronômetro
        auto fim = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> duracao = fim - inicio;

        std::cout << "Solucao encontrada!" << std::endl;
        std::cout << "Valor da funcao objetivo (Upper Bound): " << cplex.getObjValue() << std::endl;
        std::cout << "Lower bound: " << cplex.getBestObjValue() << std::endl;
        std::cout << "Gap relativo (percentual): " << cplex.getMIPRelativeGap() * 100 << "%" << std::endl;
        std::cout << "Tempo de execucao: " << duracao.count() << " segundos." << std::endl;

        // Path de escrita
        const char* arquivo_solucao = DIRETORIO_SOLUCAO_CPLEX CPLEX_PREFIXO NOME_INSTANCIA SOL;
        cplex.writeSolution(arquivo_solucao);
        std::cout << "Solucao salva em: " << arquivo_solucao << std::endl;
    }
    else {
        std::cout << "Nao foi possível encontrar uma solucao viavel." << std::endl;
    }

    env.end();

    return 0;
}

int gurobi() {

    GRBEnv env = GRBEnv(true);
    env.set("LogFile", "gurobi.log");
    env.start();

    // Path de leitura
    const char* path = DIRETORIO_MODELO NOME_INSTANCIA LP;

    GRBModel model = GRBModel(env, path);

    // Define o limite de tempo
    model.set(GRB_DoubleParam_TimeLimit, LIMITE_TEMPO);

    // Inicia o cronômetro
    auto inicio = std::chrono::high_resolution_clock::now();

    // Resolve o modelo
    model.optimize();

    // Finaliza o cronômetro
    auto fim = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> duracao = fim - inicio;

    std::cout << "Solucao encontrada!" << std::endl;
    std::cout << "Valor da funcao objetivo (Upper Bound): " << model.get(GRB_DoubleAttr_ObjVal) << std::endl;
    std::cout << "Lower bound do modelo: " << model.get(GRB_DoubleAttr_ObjBound) << std::endl;
    std::cout << "Gap relativo (percentual): " << model.get(GRB_DoubleAttr_MIPGap) * 100 << "%" << std::endl;
    std::cout << "Tempo de execucao: " << duracao.count() << " segundos." << std::endl;

    // Path de escrita
    const char* arquivo_solucao = DIRETORIO_SOLUCAO_GUROBI GUROBI_PREFIXO NOME_INSTANCIA SOL;
    model.write(arquivo_solucao);
    std::cout << "Solucao salva em: " << arquivo_solucao << std::endl;

    return 0;
}

int main() {
    //cplex();
    gurobi();
}
