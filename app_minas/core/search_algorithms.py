#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import deque
from .graph_model import Node

class SearchAlgorithms:
    """Classe que implementa os algoritmos de busca"""
    
    def __init__(self):
        self.nos_visitados = []  # Para rastrear a ordem de visitação
        self.arvore_busca = None  # Raiz da árvore de busca
        
    def busca_amplitude(self, grafo, inicio, fim):
        """
        Busca em Amplitude (BFS)
        Explora todos os nós de um nível antes de passar para o próximo
        """
        self.nos_visitados = []
        self.arvore_busca = None

        if inicio == fim:
            return [inicio], Node(estado=inicio)
            
        # Fila para BFS
        fila = deque()
        
        # Nó raiz da árvore de busca
        raiz = Node(pai=None, estado=inicio, custo=0, profundidade=0)
        self.arvore_busca = raiz
        fila.append(raiz)
        
        # Controle de nós visitados
        visitados = {inicio: raiz}
        self.nos_visitados.append(inicio)

        
        while fila:
            atual = fila.popleft()
            atual.expandido = True
            
            # Obter vizinhos
            vizinhos = grafo.obter_vizinhos(atual.estado)
            
            for vizinho, custo_aresta in vizinhos:
                # Para BFS, se o vizinho já foi visitado, não precisamos re-adicionar
                # a menos que estejamos buscando o caminho mais curto em um grafo com custos variáveis.
                # Como estamos com custo unitário, a primeira vez que é visitado é o caminho mais curto.
                # No entanto, para a árvore de busca, precisamos garantir que o pai seja o correto.
                # Para simplificar e garantir a construção correta da árvore, vamos adicionar à fila
                # apenas se não tiver sido visitado ainda, ou se for um caminho mais curto (não aplicável aqui com custo unitário).
                if vizinho not in visitados:
                    custo_total = atual.custo + custo_aresta
                    filho = Node(
                        pai=atual,
                        estado=vizinho,
                        custo=custo_total,
                        profundidade=atual.profundidade + 1
                    )
                    
                    atual.adicionar_filho(filho)
                    fila.append(filho)
                    visitados[vizinho] = filho
                    self.nos_visitados.append(vizinho)
                    
                    # Verificar se encontrou o objetivo
                    if vizinho == fim:
                        filho.objetivo = True
                        caminho = self._reconstruir_caminho(filho)
                        return caminho, self.arvore_busca
                        
        return None, self.arvore_busca
        
    def busca_profundidade(self, grafo, inicio, fim):
        """
        Busca em Profundidade (DFS)
        Explora o mais profundo possível antes de retroceder
        """
        self.nos_visitados = []
        self.arvore_busca = None

        if inicio == fim:
            return [inicio], Node(estado=inicio)
            
        # Pilha para DFS
        pilha = []
        
        # Nó raiz da árvore de busca
        raiz = Node(pai=None, estado=inicio, custo=0, profundidade=0)
        self.arvore_busca = raiz
        pilha.append(raiz)
        
        # Controle de nós visitados
        visitados = {inicio: raiz}
        self.nos_visitados.append(inicio)

        
        while pilha:
            atual = pilha.pop()
            atual.expandido = True
            
            # Obter vizinhos (em ordem reversa para manter consistência)
            vizinhos = grafo.obter_vizinhos(atual.estado)
            vizinhos.reverse()
            
            for vizinho, custo_aresta in vizinhos:
                # Para DFS, precisamos permitir revisitar nós se eles não estiverem no caminho atual
                # para explorar outros ramos da árvore de busca.
                # No entanto, para evitar ciclos infinitos, só adicionamos à pilha se não estiver no caminho atual
                # ou se for um caminho mais curto (não aplicável aqui com custo unitário).
                # Para a construção da árvore, é importante que cada nó na pilha tenha um pai correto.
                if vizinho not in visitados:
                    custo_total = atual.custo + custo_aresta
                    filho = Node(
                        pai=atual,
                        estado=vizinho,
                        custo=custo_total,
                        profundidade=atual.profundidade + 1
                    )
                    
                    atual.adicionar_filho(filho)
                    pilha.append(filho)
                    visitados[vizinho] = filho
                    self.nos_visitados.append(vizinho)
                    
                    # Verificar se encontrou o objetivo
                    if vizinho == fim:
                        filho.objetivo = True
                        caminho = self._reconstruir_caminho(filho)
                        return caminho, self.arvore_busca
                        
        return None, self.arvore_busca
        
    def busca_profundidade_limitada(self, grafo, inicio, fim, limite):
        """
        Busca em Profundidade Limitada
        DFS com limite de profundidade
        """
        self.nos_visitados = []
        self.arvore_busca = None

        if inicio == fim:
            return [inicio], Node(estado=inicio)
            
        # Pilha para DFS
        pilha = []
        
        # Nó raiz da árvore de busca
        raiz = Node(pai=None, estado=inicio, custo=0, profundidade=0)
        self.arvore_busca = raiz
        pilha.append(raiz)
        
        # Controle de nós visitados
        visitados = {inicio: raiz}
        self.nos_visitados.append(inicio)

        
        while pilha:
            atual = pilha.pop()
            atual.expandido = True
            
            # Verificar limite de profundidade
            if atual.profundidade < limite:
                # Obter vizinhos
                vizinhos = grafo.obter_vizinhos(atual.estado)
                vizinhos.reverse()
                
                for vizinho, custo_aresta in vizinhos:
                    if vizinho not in visitados:
                        custo_total = atual.custo + custo_aresta
                        filho = Node(
                            pai=atual,
                            estado=vizinho,
                            custo=custo_total,
                            profundidade=atual.profundidade + 1
                        )
                        
                        atual.adicionar_filho(filho)
                        pilha.append(filho)
                        visitados[vizinho] = filho
                        self.nos_visitados.append(vizinho)
                        
                        # Verificar se encontrou o objetivo
                        if vizinho == fim:
                            filho.objetivo = True
                            caminho = self._reconstruir_caminho(filho)
                            return caminho, self.arvore_busca
                            
        return None, self.arvore_busca
        
    def busca_aprofundamento_iterativo(self, grafo, inicio, fim, limite_inicial=1):
        """
        Busca por Aprofundamento Iterativo
        Executa DFS limitada com limite crescente
        """
        for limite in range(limite_inicial, grafo.num_nos + 1): # Itera até o número máximo de nós do grafo
            resultado, arvore = self.busca_profundidade_limitada(grafo, inicio, fim, limite)
            if resultado:
                return resultado, arvore
                
        return None, self.arvore_busca
        
    def busca_bidirecional(self, grafo, inicio, fim):
        """
        Busca Bidirecional
        Executa BFS simultaneamente do início e do fim até se encontrarem
        """
        self.nos_visitados = []
        self.arvore_busca = None
        
        if inicio == fim:
            return [inicio], Node(estado=inicio)
            
        # Filas para as duas direções
        fila_inicio = deque()
        fila_fim = deque()
        
        # Nós raiz para as duas árvores
        raiz_inicio = Node(pai=None, estado=inicio, custo=0, profundidade=0)
        raiz_fim = Node(pai=None, estado=fim, custo=0, profundidade=0)
        self.arvore_busca = raiz_inicio  # Usar a árvore do início como principal
        
        fila_inicio.append(raiz_inicio)
        fila_fim.append(raiz_fim)
        
        # Controle de nós visitados para cada direção
        visitados_inicio = {inicio: raiz_inicio}
        visitados_fim = {fim: raiz_fim}
        
        self.nos_visitados.append(inicio)
        self.nos_visitados.append(fim)
        
        while fila_inicio and fila_fim:
            # Expandir do início
            if fila_inicio:
                atual = fila_inicio.popleft()
                atual.expandido = True
                
                vizinhos = grafo.obter_vizinhos(atual.estado)
                for vizinho, custo_aresta in vizinhos:
                    if vizinho not in visitados_inicio:
                        custo_total = atual.custo + custo_aresta
                        filho = Node(
                            pai=atual,
                            estado=vizinho,
                            custo=custo_total,
                            profundidade=atual.profundidade + 1
                        )
                        
                        atual.adicionar_filho(filho)
                        visitados_inicio[vizinho] = filho
                        self.nos_visitados.append(vizinho)
                        
                        # Verificar se encontrou nó da outra busca
                        if vizinho in visitados_fim:
                            caminho = self._reconstruir_caminho_bidirecional(
                                filho, visitados_fim[vizinho]
                            )
                            return caminho, self.arvore_busca
                            
                        fila_inicio.append(filho)
                        
            # Expandir do fim
            if fila_fim:
                atual = fila_fim.popleft()
                atual.expandido = True
                
                vizinhos = grafo.obter_vizinhos(atual.estado)
                for vizinho, custo_aresta in vizinhos:
                    if vizinho not in visitados_fim:
                        custo_total = atual.custo + custo_aresta
                        filho = Node(
                            pai=atual,
                            estado=vizinho,
                            custo=custo_total,
                            profundidade=atual.profundidade + 1
                        )
                        
                        atual.adicionar_filho(filho)
                        visitados_fim[vizinho] = filho
                        
                        # Verificar se encontrou nó da outra busca
                        if vizinho in visitados_inicio:
                            caminho = self._reconstruir_caminho_bidirecional(
                                visitados_inicio[vizinho], filho
                            )
                            return caminho, self.arvore_busca
                            
                        fila_fim.append(filho)
                        
        return None, self.arvore_busca
        
    def _reconstruir_caminho(self, no_final):
        """Reconstrói o caminho do nó inicial até o nó final"""
        caminho = []
        atual = no_final
        
        while atual is not None:
            caminho.append(atual.estado)
            atual = atual.pai
            
        caminho.reverse()
        return caminho
        
    def _reconstruir_caminho_bidirecional(self, no_inicio, no_fim):
        """Reconstrói o caminho para busca bidirecional"""
        # Caminho do início até o ponto de encontro
        caminho_inicio = []
        atual = no_inicio
        while atual is not None:
            caminho_inicio.append(atual.estado)
            atual = atual.pai
        caminho_inicio.reverse()
        
        # Caminho do ponto de encontro até o fim
        caminho_fim = []
        atual = no_fim.pai  # Pular o nó de encontro para evitar duplicação
        while atual is not None:
            caminho_fim.append(atual.estado)
            atual = atual.pai
            
        # Combinar os caminhos
        return caminho_inicio + caminho_fim
        
    def obter_estatisticas(self, caminho, custo_total):
        """Retorna estatísticas da busca"""
        if not caminho:
            return "Caminho não encontrado"
            
        stats = f"Caminho encontrado: {' -> '.join(map(str, caminho))}\n"
        stats += f"Custo total: {custo_total}\n"
        stats += f"Número de nós no caminho: {len(caminho)}\n"
        stats += f"Nós visitados durante a busca: {len(self.nos_visitados)}\n"
        stats += f"Ordem de visitação: {' -> '.join(map(str, self.nos_visitados))}"
        
        return stats

