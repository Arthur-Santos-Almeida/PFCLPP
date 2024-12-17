import pprint
import numpy as np

def ler_N_P(caminho_arquivo):

    with open(caminho_arquivo, "r") as arquivo:
        N = int(arquivo.readline().strip())
        P = int(arquivo.readline().strip())
    return N, P

def ler_coeficientes(caminho_arquivo, listaConflitos, N, P):

    with open(caminho_arquivo, "r") as arquivo:
        
        # Ignora as duas primeiras linhas já lidas em ler_N_P()
        arquivo.readline()
        arquivo.readline()

        for i in range(1, N + 1):
            for a in range(1, P + 1):
                
                numConflitos = int( arquivo.readline().strip() )
                linhaEuclidiana = arquivo.readline()    # Linha da distância euclidiana ignorada
                linhaJaccard = arquivo.readline().strip().split()

                # Essa groselha toda só pra percorrer a linha de Jaccard de 2 em 2
                for conflito in range( 0, numConflitos * 2, 2 ):
                    idLabelEmConflito = int( linhaJaccard[conflito] )
                    jaccardIndex = float( linhaJaccard[conflito + 1] )

                    if idLabelEmConflito % P != 0:
                        j = int( np.ceil( idLabelEmConflito / P ) )
                    else:
                        j = int( idLabelEmConflito / P ) + 1
                    
                    parte_decimal, _ = np.modf( idLabelEmConflito / P )

                    for p in range(1, P + 1):
                        if parte_decimal * (P/p) == 1:
                            b = p + 1
                            listaConflitos.append([i,j,a,b,jaccardIndex])
                        elif parte_decimal == 0:
                            b = 1
                            listaConflitos.append([i,j,a,b,jaccardIndex])
                    
                    # if i == 0 or j == 0:
                    #     print(f"idLabelEmConflito: {idLabelEmConflito}, i: {i}, j: {j}, a: {a}, b: {b}\n")

def gerar_lp(N, P, listaConflitos, arquivo_saida):
    
    with open(arquivo_saida, "w") as f:

        f.write("Minimize\n obj:\n")
        
        # Gerar a função objetivo
        # conflito = [i,j,a,b,jaccardIndex]
        # conflito[0] = i
        # conflito[1] = j
        # conflito[2] = a
        # conflito[3] = b
        # conflito[4] = jaccardIndex
        termosFO = []
        for conflito in listaConflitos:
            if not termosFO:
                termosFO.append(f"{conflito[4]} y_{conflito[0]}_{conflito[1]}_{conflito[2]}_{conflito[3]}")
            elif termosFO:
                termosFO.append(f" + {conflito[4]} y_{conflito[0]}_{conflito[1]}_{conflito[2]}_{conflito[3]}")
        
        # Formatando a FO
        for k in range(0, len(termosFO), 10):
            f.write("".join(termosFO[k:k+10]) + "\n")

        f.write("\nSubject To\n")

        # Restrição (1): x_i^a + x_j^b - 1 <= y_{ij}
        for conflito in listaConflitos:
            f.write(f" c1_{conflito[0]}_{conflito[1]}_{conflito[2]}_{conflito[3]}: x_{conflito[0]}_{conflito[2]} + x_{conflito[1]}_{conflito[3]} - y_{conflito[0]}_{conflito[1]}_{conflito[2]}_{conflito[3]} <= 1\n")

        # Restrição (2): ∑_{a=1}^P x_i^a = 1
        for i in range(1, N + 1):
            termos_soma = " + ".join([f"x_{i}_{a}" for a in range(1, P + 1)])
            f.write(f" c2_{i}: {termos_soma} = 1\n")

        # Variáveis Y
        f.write("Bounds\n")
        for conflito in listaConflitos:
            f.write(f" 0 <= y_{conflito[0]}_{conflito[1]}_{conflito[2]}_{conflito[3]} <= 1\n")

        # Variáveis X
        f.write("Binaries\n")
        for i in range(1, N + 1):
            for a in range(1, P + 1):
                f.write(f" x_{i}_{a}\n")
        
        f.write("End\n")

def remover_duplicatas(listaConflitos):

    semDuplicatas = []

    for sublista in listaConflitos:
        if sublista not in semDuplicatas:
            semDuplicatas.append(sublista)

    return semDuplicatas

# Removendo conflitos que não são duplicadas mas são redundantes
# Ex: [1, 3, 2, 4, 0.25] e [3, 1, 4, 2, 0.25]
def remover_redundantes(listaConflitos):

    indexEquivalentes = []

    for index1 in range(0, len(listaConflitos) ):
        for index2 in range(index1 + 1, len(listaConflitos) ):
            if listaConflitos[index1][0] == listaConflitos[index2][1] and listaConflitos[index1][1] == listaConflitos[index2][0] and listaConflitos[index1][2] == listaConflitos[index2][3] and listaConflitos[index1][3] == listaConflitos[index2][2]:
                indexEquivalentes.append(index2)

    indexEquivalentes.sort(reverse = True)

    for index in indexEquivalentes:
        listaConflitos.pop(index)

    return listaConflitos

# Configuração
nome_instancia = "h2_w24_58_all"
caminho_arquivo = f"../Instances/{nome_instancia}.confl"
arquivo_saida = f"../Model/{nome_instancia}.lp"

# Parâmetros e lista auxiliar de conflitos
N, P = ler_N_P(caminho_arquivo)
listaConflitos = []

ler_coeficientes(caminho_arquivo, listaConflitos, N, P)
listaConflitos = remover_duplicatas(listaConflitos)
listaConflitos = remover_redundantes(listaConflitos)
gerar_lp(N, P, listaConflitos, arquivo_saida)

# pprint.pp(listaConflitos)
print(f"Arquivo {arquivo_saida} gerado com sucesso.")
