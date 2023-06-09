import heapq
import sys
import math
import pygame

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


def aestrela(labirinto, inicio, fim, heuristica_admissivel=True):
    custos = {}
    lista_aberta = []  
    lista_fechada = [] 

    no_inicial = No(inicio)
    no_final = No(fim)

    no_inicial.f = ((no_inicial.posicao[0] - no_final.posicao[0]) ** 2) + ((no_inicial.posicao[1] - no_final.posicao[1]) ** 2)
    heapq.heappush(lista_aberta, no_inicial)   
    custos[no_inicial.posicao] = no_inicial.f

    while lista_aberta:
        no_atual = heapq.heappop(lista_aberta)  
        lista_fechada.append(no_atual)  
        print(f"Nó visitado: {traduz_posicao(no_atual.posicao, labirinto)} de custo: {custos[no_atual.posicao]}")

        if no_atual == no_final:    
            caminho = []
            while no_atual != no_inicial:
                caminho.append(no_atual.posicao)
                no_atual = no_atual.pai
            return caminho[::-1]

        vizinhos = [(0, -1), (0, 1), (-1, 0), (1, 0)]  
        for vizinho in vizinhos:
            vizinho_posicao = (no_atual.posicao[0] + vizinho[0], no_atual.posicao[1] + vizinho[1])

            if not dentro_limites(vizinho_posicao, labirinto):  
                continue    

            if labirinto[vizinho_posicao[0]][vizinho_posicao[1]] != 0:  
                vizinho_posicao = (vizinho_posicao[0] + vizinho[0], vizinho_posicao[1] + vizinho[1])
                if not dentro_limites(vizinho_posicao, labirinto):  
                    continue    
                if labirinto[vizinho_posicao[0]][vizinho_posicao[1]] != 0:
                    continue    
                vizinho_g = no_atual.g + 3  
            else:
                vizinho_g = no_atual.g + 1  

            no_vizinho = No(vizinho_posicao, no_atual)

            if no_vizinho in lista_fechada:  
                continue    

            no_vizinho.g = vizinho_g
            if heuristica_admissivel:
                no_vizinho.h = abs((no_vizinho.posicao[0] - no_final.posicao[0])) + abs((no_vizinho.posicao[1] - no_final.posicao[1]))  # Distância de Manhattan
            else:
                no_vizinho.h = math.sqrt(((no_vizinho.posicao[0] - no_final.posicao[0]) ** 2) + ((no_vizinho.posicao[1] - no_final.posicao[1]) ** 2))  # Distãncia Euclidiana

            no_vizinho.f = no_vizinho.g + no_vizinho.h

            if adiciona_lista_aberta(lista_aberta, no_vizinho):
                heapq.heappush(lista_aberta, no_vizinho)    
                custos[no_vizinho.posicao] = no_vizinho.f
                print(f"Nó aberto: {traduz_posicao(no_vizinho.posicao, labirinto)} de custo: {custos[no_vizinho.posicao]}")

    return None


def traduz_posicao(posicao, labirinto):
    return (posicao[0] * len(labirinto[0])) + (posicao[1] + 1)


def dentro_limites(posicao, labirinto):   
    linha, coluna = posicao
    return 0 <= linha < len(labirinto) and 0 <= coluna < len(labirinto[linha])


def adiciona_lista_aberta(lista_aberta, vizinho):  
    for no in lista_aberta:
        if vizinho == no and vizinho.f >= no.f:
            return False
    return True


def printa_arvore(lista_fechada, custos):
    for no in lista_fechada:
        print(f"Nó: {no.posicao} de custo: {custos[no.posicao]}")


def main(labirinto, inicio, fim):  
    caminho = aestrela(labirinto, inicio, fim)
    return caminho

if __name__ == '__main__':
    labirinto = []  # Defina seu labirinto aqui.
    inicio = (0, 0)  # Defina o ponto de início aqui.
    fim = (5, 5)  # Defina o ponto final aqui.
    print(main(labirinto, inicio, fim))
