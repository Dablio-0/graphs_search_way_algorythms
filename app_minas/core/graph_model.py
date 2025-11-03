#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Node:
    """Classe para representar um nó na árvore de busca"""
    def __init__(self, pai=None, estado=None, custo=0, profundidade=0):
        self.pai = pai
        self.estado = estado
        self.custo = custo  # Custo acumulado do caminho
        self.profundidade = profundidade  # Profundidade na árvore
        self.filhos = []  # Lista de nós filhos
        self.expandido = False  # Se o nó foi expandido
        self.objetivo = False  # Se é o nó objetivo

    def adicionar_filho(self, filho):
        """Adiciona um filho a este nó"""
        self.filhos.append(filho)

    def __repr__(self):
        return f"Node(estado={self.estado}, custo={self.custo}, prof={self.profundidade})"


class Graph:
    """Classe para representar o grafo de túneis de mineração"""
    def __init__(self):
        self.nos = []  # Lista de nós
        self.num_nos = 0
        self.arestas = {}  # Dicionário de adjacências: {no: [(vizinho, custo), ...]}
        self.posicoes = {}  # Posições dos nós para visualização

    def adicionar_no(self, no, posicao=None):
        """Adiciona um nó ao grafo"""
        if no not in self.nos:
            self.nos.append(no)
            self.arestas[no] = []
            self.num_nos = len(self.nos)
            if posicao:
                self.posicoes[no] = posicao

    def adicionar_aresta(self, origem, destino, custo):
        """Adiciona uma aresta bidirecional"""
        if origem not in self.nos:
            self.adicionar_no(origem)
        if destino not in self.nos:
            self.adicionar_no(destino)
        self.arestas[origem].append((destino, custo))
        self.arestas[destino].append((origem, custo))

    def obter_vizinhos(self, no):
        """Retorna os vizinhos de um nó com seus respectivos custos"""
        return self.arestas.get(no, [])

    def obter_custo_aresta(self, origem, destino):
        """Retorna o custo da aresta entre dois nós"""
        for vizinho, custo in self.arestas.get(origem, []):
            if vizinho == destino:
                return custo
        return float('inf')

    def carregar_de_arquivo(self, caminho_arquivo):
        """Carrega o grafo de um arquivo de texto"""
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                linhas = arquivo.readlines()

            # Ignora comentários e linhas vazias até encontrar o número de nós
            num_nos = None
            for linha in linhas:
                linha = linha.strip()
                if linha and not linha.startswith('#'):
                    num_nos = int(linha)
                    break

            if num_nos is None:
                raise ValueError("Arquivo inválido: número de nós não encontrado.")

            # Adicionar nós
            for i in range(1, num_nos + 1):
                self.adicionar_no(i)

            # Adicionar arestas
            for linha in linhas:
                linha = linha.strip()
                if linha and not linha.startswith('#'):
                    partes = linha.split()
                    if len(partes) >= 3:
                        try:
                            origem = int(partes[0])
                            destino = int(partes[1])
                            custo = float(partes[2])
                            self.adicionar_aresta(origem, destino, custo)
                        except ValueError:
                            # Ignora linhas não numéricas (comentários, etc.)
                            continue

            return True

        except Exception as e:
            print(f"Erro ao carregar arquivo: {e}")
            return False

    def carregar_exemplo(self):
        """Carrega um grafo de exemplo (A–J)"""
        self.nos = []
        self.arestas = {}
        self.posicoes = {}

        nos_exemplo = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        for no in nos_exemplo:
            self.adicionar_no(no)

        arestas_exemplo = [
            (1, 2, 1.0), (1, 5, 1.0), (1, 6, 1.0), (1, 7, 1.0),
            (2, 3, 1.0), (2, 8, 1.0), (2, 10, 1.0),
            (3, 4, 1.0), (3, 10, 1.0),
            (4, 5, 1.0), (4, 10, 1.0),
            (5, 6, 1.0),
            (6, 7, 1.0),
            (7, 8, 1.0),
            (8, 9, 1.0),
            (9, 10, 1.0)
        ]

        for origem, destino, custo in arestas_exemplo:
            self.adicionar_aresta(origem, destino, custo)

        self.posicoes = {
            1: (0, 0),
            2: (100, 50),
            3: (200, 100),
            4: (150, -50),
            5: (50, -100),
            6: (-50, -50),
            7: (-100, 50),
            8: (-50, 100),
            9: (50, 150),
            10: (150, 150)
        }

    def obter_dados_visualizacao(self):
        """Retorna dados para visualização do grafo"""
        arestas_lista = []
        arestas_processadas = set()

        for origem in self.arestas:
            for destino, custo in self.arestas[origem]:
                aresta = tuple(sorted([origem, destino]))
                if aresta not in arestas_processadas:
                    arestas_lista.append((origem, destino, custo))
                    arestas_processadas.add(aresta)

        return {
            'nos': self.nos,
            'arestas': arestas_lista,
            'posicoes': self.posicoes
        }

    def __repr__(self):
        return f"Graph(nos={len(self.nos)}, arestas={sum(len(adj) for adj in self.arestas.values()) // 2})"
