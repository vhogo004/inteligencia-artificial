import heapq
from time import time
import csv
import tracemalloc

# Classe do quebra-cabeça 8 
class QC8:
    def __init__(self, tab, horizontal, vertical, profundidade, custo):
        self.tab = tab
        self.horizontal = horizontal
        self.vertical = vertical
        self.profundidade = profundidade
        self.custo = custo
        # heurística (f(n) = g(n) + h(n)) do algoritmo A*
        self.f = self.custo + self.profundidade
    # usa o less than para comparar qual o menor custo
    def __lt__(self,novo):
        return self.f < novo.f
# Lista de posições possíveis
linha = [0, 0, -1, 1]
coluna = [-1, 1, 0, 0]
 
# Checa se o objetivo final foi alcançado
def objetivo(tab):
    obj = [[1,2,3], [4,5,6], [7,8,0]]
    if(tab == obj):
        return 1
# Checa se as posições são válidas (Não são um elemento fora da matriz)
def valida(horizontal, vertical):
    if((horizontal >= 0 and horizontal < 3) and (vertical >= 0 and vertical < 3)):
        return 1
    
# Distância de manhattan
def manhattan(tab):
    obj = [[1,2,3], [4,5,6], [7,8,0]]
    dist = 0
    # indo em cada posição do tabuleiro
    for i in range(3):
        for l in range(3):
            # ignorando 0
            if tab[i][l] != 0:
                # divmod para coletar o quociente e o resto e atribuí para linha e coluna
                # respectivamente, quando divídimos o bloco por 3 (tamanho do tabuleiro)
                # e isso nos dá a posição que o bloco deveria estar
                lin, col = divmod(tab[i][l] -1, 3)
                # Faz o cálculo da diferença e soma a distância, gerando a distância de manhattan
                dist = dist + abs(i - lin)
                dist = dist + abs(l - col)
    return dist
 
# Método para mostrar a tab        
def mostraTab(tab):
    print()
    l = 0
 
    # Para cada linha de tab
    for i in tab:
        # Para cada elemento da linha
        for j in i:
            # Se imprime o elemento
            print(i[l]," ", end="")
            l = l + 1
        print()
        l = 0
    print()
 
# A*
def AE(tab, horizontal, vertical):
 
    # Set é mais rápido que usar uma lista quando se usa o in, devido a busca por hash dos seus elementos
    # enquanto a lista, em seu pior caso, teria de ser percorrida por inteira.
    visitado = set()
    lista = []
    # chama a distância de manhattan para o tabuleiro atual
    custo = manhattan(tab)
    # Adiciona o estado na heap(min) e marca como visitado no set
    heapq.heappush(lista,QC8(tab,horizontal,vertical,0,custo))
    visitado.add(tuple(map(tuple,tab)))
    
    while lista:
        # Tira o nó com o menor valor (para f(n))
        atual = heapq.heappop(lista)
        # Checa se estamos no estado objetivo
        if objetivo(atual.tab):
            return len(visitado), atual.profundidade
        else:
            # Dentro dos 4 movimentos, tenta gerar um válido (posição válida no tabuleiro)
            for i in range (4):
                # Se for válido;
                horizontal2 = atual.horizontal + linha[i]
                vertical2 = atual.vertical + coluna[i]
                if valida(horizontal2, vertical2):
                    tab2 = [linha.copy() for linha in atual.tab]
                    # faz a troca dos valores entre dois tabuleiros (um com o atual e o outro com o vizinho)
                    tab2[atual.horizontal][atual.vertical], tab2[horizontal2][vertical2] = tab2[horizontal2][vertical2], tab2[atual.horizontal][atual.vertical]
                    tabi = tuple(map(tuple, tab2))
                    # Caso o estado atual agora não tenha sido visitado, calcula a distancia de manhattan e adiciona a heap
                    if tabi not in visitado:
                        visitado.add(tabi)
                        custo2 = manhattan(tab2)
                        tab3 = QC8(tab2, horizontal2, vertical2, atual.profundidade + 1, custo2)
                        heapq.heappush(lista,tab3)
    # Caso de erro
    print("Erro na instância! Objetivo não encontrado")                      
    return -1,-1
 
# Inicializa variáveis
# Lista de tempo tomado para cada iteração
ListaTempo = []    
ListaMemoria = []
# Lista de passos tomado para cada iteração
ListaPassos = []
# Lista de profundidade onde foi encontrado o objetivo, se foi
ListaProf= []
 
# Lê o arquivo CSV
instancias = []
with open('ed02-puzzle8.csv') as fp:
    arquivo = fp.readlines()
    for linhaarq in arquivo[1:]:
        linhaarq = linhaarq.strip()
        puzzlearq = [int(token) for token in linhaarq.split(',')]
        instancias.append(puzzlearq)
 
# Separa os valores lidos em formato reconhecível para os algoritmos de busca.
# A cada 3 valores lidos, temos uma lista(1). A cada 3 listas(1), temos outra lista(2).
# Cada uma dessas listas(2) é inserida em uma lista(3).
# Assim, cada valor dessa lista(3) é uma instância do programa
lista1 = []
lista2 = []
lista3 = []
 
k = 0
for i in instancias:
 
    for j in i:
        lista3.append(j)
 
        if(k == 2):
            lista2.append(lista3)
            lista3 = []
            k = 0
 
        else:      
            k = k + 1
    lista1.append(lista2)
    lista2 = []
 
o = 1
# Chama o algoritmo para cada instância
for i in lista1:
    passos = 0
    prof = 0
    instancia = i  
 
    print("Instância ", o, "começando.")  
    print("Puzzle inicial: ")
    mostraTab(instancia)
 
    # Var básicas
    horizontal = -1
    vertical = -1
 
    # Ajusta a posição do espaço vazio
    for i in range(3):
        for j in range(3):
            if instancia[i][j] == 0:
                horizontal = i
                vertical = j
 
    # Chama o algoritmo para uma instância, junto com a medição de memória e medição de tempo
    tracemalloc.start()
    memInicio = tracemalloc.get_traced_memory()[0]
    inicio = time()
    passos, prof = AE(instancia, horizontal, vertical)
    fim = time()
    memFim = tracemalloc.get_traced_memory()[0]
    tracemalloc.stop()
    print("Terminado instância ", o)
    o = o + 1
 
    # O tempo, memória, passos e profundidade da instância são adicionados as suas listas respectivas
    ListaTempo.append(fim - inicio)
    ListaMemoria.append((memFim - memInicio)/ 10**3)
    ListaPassos.append(passos)
    ListaProf.append(prof)
    print()
 
print("Dados de cada instância")
for o in range (10):
    print("[", o + 1, "] | Passos: ", ListaPassos[o], "| Profundidade: ", ListaProf[o], "| Memória: ", ListaMemoria[o], "KBs" ,"| Tempo: ", ListaTempo[o] , "segundos")
 
