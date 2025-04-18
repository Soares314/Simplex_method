import numpy as np

## Recebe uma matriz A e procura dentro dela uma matriz indentidade. Retornando os indices da matriz indentidade e os que não pertencem a ela.
def indentidade_search(A):
    index_base = []
    index_nao_base = []
    index_nulo = []
    for i in range(len(A)):
        for j in range(len(A[0])):
            if(j not in index_nao_base or j not in index_base):
                if( A[i][j] != 1 and A[i][j] != 0 and j not in index_nao_base):
                    index_nao_base.append(j)
                    continue
                elif( A[i][j] == 1):
                    for x in range(len(A)):
                        if( A[x][j] != 0 and x != i):
                            if(j not in index_nao_base):
                                index_nao_base.append(j)
                            break
                    if( j not in index_nao_base):
                        index_base.append(j)
   
    return {
        'base' : index_base, 
        'nao_base' : index_nao_base
    }

## Troca os indices entre a base e a não base, buscando o valor minimizante para as restrições.
def troca_de_base(index, entra_base, x, y):
    bases = []
    
    for i in range(len(y)):
    
        if y[i] != 0:
            bases.append(float((x[i]/y[i]).item()))
        else:
            bases.append(float('inf'))
    sai_base = bases.index(min(bases))
    j = index['base'][sai_base]
    index['base'][sai_base] = index['nao_base'][entra_base]
    index['nao_base'][entra_base] = j
    """
    print("bases: ", bases)
    print("Index_base: ", index['base'])
    print("Index_nao_base: ", index['nao_base'])
    """

## Busca a solução ótima, verificando se a solução é viável e se não existe mais variáveis que possam ser trocadas entre a base e a não base.
def max(index, A, b, c):
    otimidade = True
    valor_corrigir = 0
    base = A[:, index['base']]
    nao_base = A[:, index['nao_base']]
    c_base = c[0, index['base']]
    c_nao_base = c[0, index['nao_base']]
    base_inv = np.linalg.inv(base)
    u = c_base @ base_inv
    x = base_inv @ b
    """
    print("Base matrix (A[:, index['base']]):\n", base)
    print("Non-base matrix (A[:, index['nao_base']]):\n", nao_base)
    print("c_base (c[0, index['base']]):\n", c_base)
    print("c_nao_base (c[0, index['nao_base']]):\n", c_nao_base)
    print("Inverse of base matrix (base_inv):\n", base_inv)
    print("u (c_base @ base_inv):\n", u)
    print("x: \n", x)
    """
    solucao = u @ b
    z = []
    for i in range(len(nao_base[0])):
        z.append(u @ nao_base[:, i])
        z[i] = float(z[i])
        #print("{} - {}".format(z[i], c_nao_base[i]))
        if z[i] - c_nao_base[i] < 0:
            otimidade = False
            if(i == 0):
                valor_corrigir = i
            else:
                if (z[valor_corrigir] - c_nao_base[valor_corrigir]) > (z[i] - c_nao_base[i]):
                    valor_corrigir = i
    print("\n")
    if(otimidade == False):
        y = base_inv @ nao_base[:, valor_corrigir]
        troca_de_base(index, valor_corrigir, x, y)
        return max(index, A, b, c)
    else:
        return { 
            'index' : index, 
            'solucao': solucao, 
            'x': x
        }        

## Torna visível a solução ótima encontrada, mostrando os valores de x e o valor ótimo.
def otimo(index, maior, valor_nao_zero):
    
    print("Solução ótima encontrada!")
    tamanho_x = len(index['base']) + len(index['nao_base'])
    x = [0] * tamanho_x
    for i, item in enumerate(index['base']):
        item = int(item)
        valor_nao_zero[i] = float(valor_nao_zero[i].item())
        x[item] = valor_nao_zero[i]
    for i in range(tamanho_x):
        print("x_{}: ".format(i+1), x[i])
    print("Valor ótimo: ", maior)

## Função principal que executa o algoritmo Simplex.
def main():
    A = np.array([[1, 1, 1, 0], [0.2, 0.5, 0, 1]])
    b = np.array([[100], [30]]) 
    c = np.array([[0.1, 0.15, 0, 0]])
    index = indentidade_search(A)
    #"""
    print("Index_base: ", index['base'])
    print("Index_nao_base: ", index['nao_base'])
    #"""
    """
    print("Bases: ", indexes[0])
    print("Não bases: ", indexes[1])
    print("Base: ", base)
    print("Não base: ", nao_base)
    """
    #print("Max: ", max(index, A, b, c))
    resolucao = max(index, A, b, c)
    otimo(resolucao['index'], resolucao['solucao'], resolucao['x'])
    
main()