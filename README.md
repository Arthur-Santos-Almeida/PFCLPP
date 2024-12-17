📂 Estrutura do Projeto
1️⃣ Instances

📁 Descrição:
Contém as 6 instâncias (conjunto de dados bruto) que foram analisadas no trabalho.
2️⃣ lp_generator

🐍 Descrição:
Contém um script em Python responsável por:

    Ler um arquivo de instância da pasta Instances.
    Interpretá-lo e gerar um arquivo .lp com a representação algébrica correspondente, seguindo o modelo matemático especificado no artigo.

3️⃣ Model

📝 Descrição:
Pasta que contém arquivos .lp (Linear Program), representando a forma algébrica de uma instância específica.
4️⃣ Solver

⚙️ Descrição:
Contém um script em C++ usado para:

    Chamar as bibliotecas do CPLEX e Gurobi.
    Ler o arquivo .lp do diretório especificado (pasta Model).
    Configurar o tempo limite para execução.
    Escrever a solução obtida em outro diretório (pasta Solution).

5️⃣ Solution

📄 Descrição:
Pasta com arquivos .sol gerados pelas ferramentas CPLEX e Gurobi. Estes arquivos contêm:

    A melhor solução obtida, ou seja, os valores de todas as variáveis na representação algébrica do problema.
    O valor da função objetivo alcançada pela solução.
