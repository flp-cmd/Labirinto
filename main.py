import heapq

labirinto = [[0, 1, 0, 0, 0],
             [0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0],
             [0, 0, 0, 1, 0],
             [0, 0, 0, 1, 0],
             [0, 1, 0, 1, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0],
             [0, 0, 0, 1, 0],
             [0, 1, 0, 1, 0],
             [0, 0, 0, 0, 0]]

inicio = (0, 0)
fim = (4, 4)


class No:
    def __init__(self, posicao, pai=None):
        self.posicao = posicao
        self.pai = pai
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.posicao == other.posicao

    def __lt__(self, other):
        return self.f < other.f


def aestrela(labirinto, inicio, fim):
    no_inicial = No(inicio)
    no_final = No(fim)

    lista_aberta = []   # Lista de nós a serem explorados
    lista_fechada = []  # Lista de nós já explorados

    heapq.heappush(lista_aberta, no_inicial)    # Adiciona o nó inicial na lista de nós abertos

    while lista_aberta:
        no_atual = heapq.heappop(lista_aberta)  # Seleciona o nó de menor custo f da lista de nós abertos
        lista_fechada.append(no_atual)  # Adiciona o nó atual na lista de nós explorados

        if no_atual == no_final:    # Se chegou ao nó final, constrói e retorna o caminho percorrido
            caminho = []
            while no_atual != no_inicial:
                caminho.append(no_atual.posicao)
                no_atual = no_atual.pai
            return caminho[::-1]

        vizinhos = [(0, -1), (0, 1), (-1, 0), (1, 0)]   # Posições dos vizinhos: acima, abaixo, esquerda, direita
        for vizinho in vizinhos:
            vizinho_posicao = (no_atual.posicao[0] + vizinho[0], no_atual.posicao[1] + vizinho[1])

            if vizinho_posicao[0] > (len(labirinto) - 1) or vizinho_posicao[0] < 0 or vizinho_posicao[1] > (len(labirinto[len(labirinto)-1]) - 1) or vizinho_posicao[1] < 0:  # Verificando se o vizinho está fora do labirinto
                continue    # Ignora vizinhos fora dos limites do labirinto

            if labirinto[vizinho_posicao[0]][vizinho_posicao[1]] != 0:  # Se o vizinho é uma parede, pula para o próximo vizinho após a parede
                vizinho_posicao = (vizinho_posicao[0] + vizinho[0], vizinho_posicao[1] + vizinho[1])
                if vizinho_posicao[0] > (len(labirinto) - 1) or vizinho_posicao[0] < 0 or vizinho_posicao[1] > (len(labirinto[len(labirinto) - 1]) - 1) or vizinho_posicao[1] < 0:  # Verificando se o vizinho está fora do labirinto
                    continue    # Ignora vizinhos após a parede que estão fora dos limites do labirinto
                if labirinto[vizinho_posicao[0]][vizinho_posicao[1]] != 0:
                    continue    # Ignora vizinhos após a parede que também são paredes
                vizinho_g = no_atual.g + 3  # Atualiza o custo g do vizinho com 3 (pulo sobre a parede)
            else:
                vizinho_g = no_atual.g + 1  # Atualiza o custo g do vizinho com 1 (movimento normal)

            no_vizinho = No(vizinho_posicao, no_atual)

            if no_vizinho in lista_fechada:  # Verificando se o vizinho já foi visitado
                continue    # Ignora vizinhos já explorados

            no_vizinho.g = vizinho_g
            no_vizinho.h = ((no_vizinho.posicao[0] - no_final.posicao[0]) ** 2) + ((no_vizinho.posicao[1] - no_final.posicao[1]) ** 2)
            no_vizinho.f = no_vizinho.g + no_vizinho.h

            if adiciona_lista_aberta(lista_aberta, no_vizinho):
                heapq.heappush(lista_aberta, no_vizinho)    # Adiciona o vizinho na lista de nós abertos

    return None  # Se não encontrar um caminho, retorna None


def adiciona_lista_aberta(lista_aberta, vizinho):   # Função que retorna True se o vizinho deve ser adicionado à lista de nós abertos
    for no in lista_aberta:
        if vizinho == no and vizinho.f >= no.f:
            return False
    return True


def main():  # Função principal que roda a função A* e retorna o caminho percorrido
    caminho = aestrela(labirinto, inicio, fim)
    return caminho


if __name__ == '__main__':
    main()
