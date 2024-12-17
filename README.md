# 1) Instances
- As 6 instâncias (conjunto de dados bruto) analisadas no trabalho.

# 2) lp_generator
- Contém um script em Python usado para ler um arquivo de instância [1], interpretá-lo, e escrever um arquivo .lp [3] com a representação algébrica correspondente de acordo com o modelo matemático especificado no artigo.

# 3) Model
- Arquivos .lp (linear program), modelos que representam a forma algébrica de uma instância específica.

# 4) Solver
- Contém um script em C++ usado para chamar as bibliotecas do CPLEX e Gurobi, ler o .lp [3] no diretório especificado, definir o tempo limite, e escrever a solução obtida [5] em outro diretório;
- É necessário configurar o ambiente para que as bibliotecas sejam importadas e usadas adequadamente. Como IDE foi usado o Visual Studio 2022.

# 5) Solution
- Arquivos .sol para CPLEX e Gurobi. São os arquivos que contém a melhor solução obtida, ou seja, armazenam os valores de todas as variáveis da forma algébrica do problema. Armazenam também o valor da função objetivo alcançada pela solução.
