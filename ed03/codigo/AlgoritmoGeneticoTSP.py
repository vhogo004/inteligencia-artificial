import random
import math
from time import time

# Parser dos CSV e criação da lista de cidades
def leCSV(o):
    cidades = []

    # Lê o CSV
    nomeArq = 'tsp_' + str(o) + '.csv'
    with open(nomeArq) as fp:
        arquivo = fp.readlines()
        # Para cada linha
        for linhaarq in arquivo[1:]:
            linhaarq = linhaarq.strip()
            cidArq = [float(token) for token in linhaarq.split(',')]
            # Adiciona uma lista dos valores na lista de cidades
            cidades.append([str(int(cidArq[0])), (cidArq[1]), (cidArq[2])])

    return cidades


# Método para calcular a distância entre as cidades
def distanciaCid(cidades):
    soma = 0
    # Acessa cada cidade junto com a próx da lista
    for i in range(len(cidades) - 1):
        cid1 = cidades[i]
        cid2 = cidades[i+1]

        # Faz calculo da distância euclidiana (Com as coordenadas x e y)
        coord1 = math.pow(cid2[1] - cid1[1], 2)
        coord2 = math.pow(cid2[2] - cid1[2],2)
        dist = math.sqrt(coord1 + coord2)

        # Soma a distância percorrida entre as duas cidades
        soma = soma + dist
    
    cid1 = cidades[0]
    cid2 = cidades[-1]
    
    # Cálculo do retorno ao ponto de origem (cidade inicial)

    coord1 = math.pow(cid2[1] - cid1[1], 2)
    coord2 = math.pow(cid2[2] - cid1[2],2)
    dist = math.sqrt(coord1 + coord2)
    
    soma = soma + dist

    return soma

# Seleciona a população
def escPopulacao(cidades, tam):
    populacao = []

    for i in range(tam):
        # Cria uma copia da lista de cidades
        copiaCid = cidades.copy()
        # Embaralha as cidades, gerando uma nova lista, com o shuffle
        random.shuffle(copiaCid)
        # Faz o cálculo da distância total para a nova lista
        dist = distanciaCid(copiaCid)
        # Adiciona a lista de população a distância e a lista
        populacao.append([dist, copiaCid])
    
    # Ordena a lista da população em ordem crescente e pega o melhor cromossomo (Com menor distância) com o sorted
    fit = sorted(populacao)[0]

    # Devolve a população gerada e o cromossomo mais apto
    return populacao, fit

# Algoritmo guloso
def Gulosa(cidades):
    # Cidade inicial aleatória
    cidInicial = random.choice(cidades)
    # Para cidades não visitadas ainda; Deve ter tipo alterado para tupla
    nvis = set(tuple(cid) for cid in cidades)
    # Tira a primeira, pois já estamos
    nvis.remove(tuple(cidInicial))
    atual = cidInicial
    # Caminho percorrido
    cam = [cidInicial]

    # Enquanto tiver cidades não visitadas
    while nvis:
        prox = None
        # Menor distância como máxima inicialmente
        menDist = float('inf')
        # Para cada cidade ainda restante
        for vt in nvis:
            v = list(vt)
            # Cálculo da distância euclidiana
            coord1 = math.pow(v[1] - atual[1], 2)
            coord2 = math.pow(v[2] - atual[2],2)
            dist = math.sqrt(coord1 + coord2)

            # Se a distância for menor que a menor até o momento
            if dist < menDist:
                menDist = dist
                proxt = vt
                prox = v

        # Adiciona a lista do caminho que está sendo percorrido
        if prox:
            cam.append(prox)
            # Marca que visitamos
            nvis.remove(proxt)
            atual = prox
        else:
            break

    # Cálculo da distância total
    dist = distanciaCid(cam)
    return [dist,cam]

# Seleciona a população com a heurística gulosa
def escPopulacaoGulosa(cidades, tam):
    populacao = []
    # Quantidade da população que sera usado a heurística
    qtd = tam // 10
    for i in range(qtd):
        populacao.append(Gulosa(cidades.copy()))

    for i in range(tam - qtd):
        # Cria uma copia da lista de cidades
        copiaCid = cidades.copy()
        # Embaralha as cidades, gerando uma nova lista, com o shuffle
        random.shuffle(copiaCid)
        # Faz o cálculo da distância total para a nova lista
        dist = distanciaCid(copiaCid)
        # Adiciona a lista de população a distância e a lista
        populacao.append([dist, copiaCid])
    
    # Ordena a lista da população em ordem crescente e pega o melhor cromossomo (Com menor distância) com o sorted
    fit = sorted(populacao)[0]

    # Devolve a população gerada e o cromossomo mais apto
    return populacao, fit

# Método para o Algoritmo Genético 
def genetico(populacao, numCid, tamSelecao, mutacao,crossover, estagnacao):
    # Geração atual
    gen = 0
    
    # Caso critério de estagnação esteja sendo utilizado
    if(estagnacao == 1):
        maxNaoMelhora = 30 # Número limite de gerações estagnadas (Pode ser alterado)

        naoMelhora = 0 
        melhor = sorted(populacao)[0][0]

    # Número fixo de gerações geradas
    for i in range(200):
        npopulacao = []
        
        # Seleciona os dois melhores cromossomos usando o Elitismo e insere-os na lista nova (nova geração)
        npopulacao.append(sorted(populacao)[0])
        npopulacao.append(sorted(populacao)[1])


        # Acha os cromossomos restantes para a nova geração 
        for i in range (int((len(populacao) - 2) / 2)):

            # Faz o crossover
            # Faz a seleção de dois cromossomos por torneio

            # Caso o crossover seja de um ponto;
            if crossover == 1:
                # O melhor dos participantes aleatórios é selecionado da população para cada pai por torneio
                pai1 = sorted(random.choices(populacao, k = tamSelecao))[0]
                pai2 = sorted(random.choices(populacao, k = tamSelecao))[0]
                
                # Usa a configuração específicada para fazer o crossover;
                # Marca um ponto aleatório de acordo com o número de cidades;
                # Usa para demarcar o crossover
                ponto = random.randint(0, numCid -1)
                
                # Pega uma parte do cromossomo pai 1, do seu começo até um certo ponto
                filho1 = pai1[1][0:ponto]
                # A segunda parte é coletada do pai 2, ignorando cidades já presentes
                for j in pai2[1]:
                    # Caso cidade não esteja no cromossomo filho 1, adiciona a sua lista
                    # Caso ela esteja, é ignorada
                    if (j in filho1) == False:
                        # Adiciona cidade ao filho 1
                        filho1.append(j)

                # Mesma operação, mas agora coleta primeira parte de pai 2, e segunda de pai 1, para o filho 2
                filho2 = pai2[1][0:ponto]
                for j in pai1[1]:
                    if (j in filho2) == False:
                        filho2.append(j)

            # Caso o crossover seja de dois pontos; Mesmas operações que em cima
            elif crossover == 2:
                pai1 = sorted(random.choices(populacao, k = tamSelecao))[0]
                pai2 = sorted(random.choices(populacao, k = tamSelecao))[0]
                
                # Demarca um segundo ponto também
                ponto1 = random.randint(0, numCid -2)
                ponto2 = random.randint(ponto1 +1, numCid -1)
                
                # Demarca area central entre os dois pontos
                p1 = pai1[1][ponto1:ponto2 +1]
                # Preenche lista de filho com None, para poder substituir o valor no local correto
                filho1 = [None] * numCid
                # Preenche area central do filho com os valores demarcados do pai
                filho1[ponto1:ponto2 +1] = p1

                # Pega area após a demarcada; Usa o mod para, caso o núm max seja alcançado,
                # possa retornar ao começo, e não tente sobrepor um espaço "não existente"
                p1_2 = 0
                for j in pai2[1]:
                    # Se cidade encontrada não estiver adicionada
                    if (j in p1) == False:
                        # Caso o segmento seja alcançado, durante ele, não substitui nenhum valor;
                        while p1_2 >= ponto1 and p1_2 <= ponto2:
                            p1_2 = p1_2 + 1
                        # Caso a posição já esteja ocupada por algo, não substitui nenhum valor
                        while filho1[p1_2] is not None:
                            p1_2 = p1_2 + 1

                        filho1[p1_2] = j

                # Mesmo processo para o filho 2
                p2 = pai2[1][ponto1:ponto2 +1]
                filho2 = [None] * numCid
                filho2[ponto1:ponto2 +1] = p2
                p2_2 = 0
                for j in pai1[1]:
                    if (j in p2) == False:
                        while p2_2 >= ponto1 and p2_2 <= ponto2:
                            p2_2 = p2_2 + 1

                        while filho2[p2_2] is not None:
                            p2_2 = p2_2 + 1

                        filho2[p2_2] = j

            # Caso o crossover seja uniforme
            elif crossover == 3:
                 # O melhor dos participantes aleatórios é selecionado da população para cada pai
                pai1 = sorted(random.choices(populacao, k = tamSelecao))[0]
                pai2 = sorted(random.choices(populacao, k = tamSelecao))[0]
                        
                filho1 = []
                filho2 = []

                # Para cada cidade
                for j in range(numCid):
                    # Randomiza o pai herdado;
                    if random.random() < 0.5:
                        # Caso a cidade do pai não esteja no filho; Adiciona
                        if (pai1[1][j] in filho1) == False:
                            filho1.append(pai1[1][j])
                        # Caso a cidade do pai já esteja no filho; Não adiciona ela, devemos achar outra
                        else:
                            for cid in pai1[1]:
                                if (cid in filho1) == False:
                                    filho1.append(cid)
                                    break

                        if (pai2[1][j] in filho2) == False:    
                            filho2.append(pai2[1][j])

                        else:
                            for cid in pai2[1]:
                                if (cid in filho2) == False:
                                    filho2.append(cid)
                                    break
                    else:
                        if (pai2[1][j] in filho1) == False:
                            filho1.append(pai2[1][j])
                        else:
                            for cid in pai2[1]:
                                if (cid in filho1) == False:
                                    filho1.append(cid)
                                    break
                        if (pai1[1][j] in filho2) == False:   
                            filho2.append(pai1[1][j])
                        else:
                            for cid in pai1[1]:
                                if (cid in filho2) == False:
                                    filho2.append(cid)
                                    break

            # Faz a mutação (Caso caia na probabilidade)
            if random.random() < mutacao:
                # Ponto aleatório demarcado
                ponto1 = random.randint(0, numCid -1)
                ponto2 = random.randint(0, numCid -1)

                # Troca a posição entre as duas cidades (de acordo com os pontos) para o filho 1
                filho1[ponto1], filho1[ponto2] = (filho1[ponto2], filho1[ponto1])
                
                # Realiza o mesmo processo para o cromossomo filho 2
                ponto1 = random.randint(0, numCid -1)
                ponto2 = random.randint(0, numCid -1)

                filho2[ponto1], filho2[ponto2] = (filho2[ponto2], filho2[ponto1])
            
            # Adiciona os novos cromossomos a lista da nova população então, com a distância calculada
            npopulacao.append([distanciaCid(filho1), filho1])
            npopulacao.append([distanciaCid(filho2), filho2])
        
        # Substitui a população antiga com a nova população
        populacao = npopulacao
        # Incrementa o número de gerações
        gen = gen + 1

        atual = sorted(populacao)[0][0]
        # Mostra a geração atual e a melhor distância encontrada
        if gen % 10 == 0:
            print("Geração: ", gen, " | Melhor distância: ", atual)
        

        # Caso critério de estagnação esteja sendo usado;
        if(estagnacao == 1):
            # Checa se melhorou
            if(atual < melhor):
                melhor = atual
                naoMelhora = 0
            # Caso não, incrementa
            else:
                naoMelhora = naoMelhora + 1
            # Caso o limite de estagnações foi alcançado
            if(naoMelhora >= maxNaoMelhora):
                print("Estagnou durante ", maxNaoMelhora, "gerações. Parada forçada.")
                break

    # Resultado final
    res = sorted(populacao)[0]

    return res, gen

# Main
def main():
    # Configurações iniciais
    tamPopulacao = 2000
    
    tamSelecao = 4

    # Chance de mutação
    mutacao = 0.01 # Escala de 0 a 1.0; Quanto maior, maior a chance de mutar

    # Crossover
    crossover = 2 # 1 Para um ponto; 2 Para dois pontos; 3 para uniforme

    # Parada por critério de estagnação; Convergência para solução ótima utilizada
    estagnacao = 1 # 1 Para ter estagnacao, 0 para não ter
    
    # Método usado para a geração da população inicial
    metodoPopulacao = 0 # 0 para população aleatória; 1 Para fazer uso de heurística;


    # Listas para guardar os dados de cada instância:
    listaTempo = []
    listaGen = []
    listaFitInicio = []
    listaFitFim = []
    # Loop while para ler todas instâncias e usar o algoritmo para cada
    o = 1
    while o <= 10:
        print("| Instância", o)
        # Parser do CSV
        cidades = leCSV(o)

        # Começa a contar o tempo
        inicio = time()

        # Gera a população inicial
        if(metodoPopulacao == 0):
            populacaoInicial, fitInicial = escPopulacao(cidades, tamPopulacao)
        elif(metodoPopulacao == 1):
            populacaoInicial,fitInicial = escPopulacaoGulosa(cidades,tamPopulacao)
        else:
            print("| Método de população inicial inválido! Finalizando programa")
            raise Exception("Método de inicialização de população inválido")

        # Roda o algoritmo genetico para encontrar o melhor cromossomo
        res, gen = genetico(populacaoInicial, len(cidades), tamSelecao, mutacao, crossover,estagnacao)

        # Termina de contar o tempo
        fim = time()

        # Mostra as informações finais
        print()
        print("| Geração: " + str(gen))
        print("| Melhor cromossomo inicial: " + str(fitInicial[0]))
        print("| Melhor cromossomo final: " + str(res[0]))
        print("| Tempo levado: ", fim - inicio)
        print()

        listaGen.append(gen)
        listaFitInicio.append(fitInicial[0])
        listaFitFim.append(res[0])
        listaTempo.append (fim - inicio)
        o = o + 1

    
    print("| Dados de cada instância")
    for o in range(10):
        print("[", o + 1, "] | Gerações: ", listaGen[o], "| Melhor custo Inicial: ", listaFitInicio[o], "| Melhor custo final", listaFitFim[o] ,"| Tempo: ", listaTempo[o] , "segundos")
    
    for o in range(10):
        print( o + 1, "&", f"{listaFitFim[o]:.3f}" ,"&", f"{listaTempo[o]:.4f}", "\\\\")
main()


