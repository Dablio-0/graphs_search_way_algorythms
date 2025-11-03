from collections import deque
from .node_p import NodeP
from math import sqrt, fabs
from .graph_model import Graph

class SearchAlgorithmsP:
    """Classe que implementa os algoritmos de busca ponderados"""
    
    def __init__(self):
        self.nos_visitados = []  # Para rastrear a ordem de visitação
        self.arvore_busca = None  # Raiz da árvore de busca
        
    def _reconstruir_caminho(self, no_final):
        """Reconstrói o caminho do nó inicial até o nó final"""
        caminho = []
        atual = no_final
        
        while atual is not None:
            caminho.append(atual.estado)
            atual = atual.pai
            
        caminho.reverse()
        return caminho
        
    def _inserir_ordenado(self, lista, no):
        """Insere o nó na lista mantendo-a ordenada pelo valor v1 (f(n) ou h(n))"""
        for i, n in enumerate(lista):
            if no.v1 < n.v1:
                lista.insert(i, no)
                return
        lista.append(no)
        
    def _heuristica_grafo(self, grafo: Graph, no_atual, no_destino):
        """
        Heurística simples para grafos (ex: distância euclidiana se posições disponíveis).
        Como não temos um mapa de posições 2D para todos os nós, usaremos uma heurística
        simples e admissível (custo 0) ou uma heurística mais complexa se houver dados.
        
        Para fins de demonstração e seguindo a lógica do arquivo do professor,
        vamos usar uma heurística baseada em um valor fixo (simulando uma tabela de distâncias).
        
        NOTA: O arquivo do professor usava uma matriz de valores aleatórios.
        Para um grafo genérico, a heurística mais segura é 0 (BFS).
        Vamos simular uma heurística simples baseada na diferença de IDs, que é admissível
        se o custo real for sempre maior ou igual a essa diferença.
        """
        # Se o grafo tiver posições, podemos usar a distância euclidiana.
        if grafo.posicoes:
            try:
                pos_atual = grafo.posicoes[no_atual]
                pos_destino = grafo.posicoes[no_destino]
                # Distância euclidiana
                return sqrt((pos_atual[0] - pos_destino[0])**2 + (pos_atual[1] - pos_destino[1])**2)
            except KeyError:
                # Se a posição não estiver definida, retorna 0 (heurística admissível)
                return 0
        
        # Heurística de distância Manhattan (admissível se custo >= 1)
        # return fabs(no_atual - no_destino)
        
        # Heurística admissível mais simples (0)
        return 0

    # -----------------------------------------------------------------------------
    # CUSTO UNIFORME
    # -----------------------------------------------------------------------------
    def custo_uniforme(self, grafo: Graph, inicio, fim):
        """Busca de Custo Uniforme (UCS)"""
        self.nos_visitados = []
        self.arvore_busca = None
        
        if inicio == fim:
            return [inicio], NodeP(estado=inicio, v1=0, v2=0)
            
        # Fila de prioridade (deque com inserção ordenada)
        lista = deque()
        
        # v1 = g(n) (custo acumulado)
        raiz = NodeP(pai=None, estado=inicio, v1=0, v2=0)
        self.arvore_busca = raiz
        lista.append(raiz)
        
        # Controle de nós visitados/expandidos
        visitado = {inicio: raiz}
        
        while lista:
            # remove o nó com menor v1 (custo acumulado)
            atual = lista.popleft()
            atual.expandido = True
            self.nos_visitados.append(atual.estado) # Adiciona o nó sendo expandido à ordem de visitação
            
            # Chegou ao objetivo
            if atual.estado == fim:
                caminho = self._reconstruir_caminho(atual)
                return caminho, self.arvore_busca, atual.v2
            
            # Gera sucessores
            vizinhos = grafo.obter_vizinhos(atual.estado)
            
            for vizinho, custo_aresta in vizinhos:
                # custo acumulado até o sucessor
                v2 = atual.v2 + custo_aresta
                v1 = v2 # Para UCS, f(n) = g(n)
                
                # Não visitado ou custo melhor
                if (vizinho not in visitado) or (v2 < visitado[vizinho].v2):
                    filho = NodeP(pai=atual, estado=vizinho, v1=v1, v2=v2)
                    
                    # Atualiza o nó visitado
                    if vizinho in visitado:
                        # Remove o nó antigo da lista (se estiver lá)
                        try:
                            lista.remove(visitado[vizinho])
                        except ValueError:
                            pass # Já foi removido ou não estava na lista
                    
                    visitado[vizinho] = filho
                    atual.adicionar_filho(filho)
                    self._inserir_ordenado(lista, filho)
                    
        return None, self.arvore_busca, 0

    # -----------------------------------------------------------------------------
    # GREEDY
    # -----------------------------------------------------------------------------
    def greedy(self, grafo: Graph, inicio, fim):
        """Busca Gulosa (Greedy Best-First Search)"""
        self.nos_visitados = []
        self.arvore_busca = None
        
        if inicio == fim:
            return [inicio], NodeP(estado=inicio, v1=0, v2=0)
            
        # Fila de prioridade (deque com inserção ordenada)
        lista = deque()
        
        # v1 = h(n) (heurística)
        h_inicial = self._heuristica_grafo(grafo, inicio, fim)
        raiz = NodeP(pai=None, estado=inicio, v1=h_inicial, v2=0)
        self.arvore_busca = raiz
        lista.append(raiz)
        
        # Controle de nós visitados/expandidos
        visitado = {inicio: raiz}
        
        while lista:
            # remove o nó com menor v1 (heurística)
            atual = lista.popleft()
            atual.expandido = True
            self.nos_visitados.append(atual.estado) # Adiciona o nó sendo expandido à ordem de visitação
            
            # Chegou ao objetivo
            if atual.estado == fim:
                caminho = self._reconstruir_caminho(atual)
                return caminho, self.arvore_busca, atual.v2
            
            # Gera sucessores
            vizinhos = grafo.obter_vizinhos(atual.estado)
            
            for vizinho, custo_aresta in vizinhos:
                # custo acumulado até o sucessor
                v2 = atual.v2 + custo_aresta
                # v1 = h(n)
                v1 = self._heuristica_grafo(grafo, vizinho, fim)
                
                # Não visitado ou custo melhor (para Greedy, a condição de re-visita é mais complexa,
                # mas para manter a simplicidade e evitar ciclos, vamos usar a condição de custo acumulado)
                if (vizinho not in visitado) or (v2 < visitado[vizinho].v2):
                    filho = NodeP(pai=atual, estado=vizinho, v1=v1, v2=v2)
                    
                    # Atualiza o nó visitado
                    if vizinho in visitado:
                        try:
                            lista.remove(visitado[vizinho])
                        except ValueError:
                            pass
                    
                    visitado[vizinho] = filho
                    atual.adicionar_filho(filho)
                    self._inserir_ordenado(lista, filho)
                    
        return None, self.arvore_busca, 0

    # -----------------------------------------------------------------------------
    # A ESTRELA
    # -----------------------------------------------------------------------------
    def a_estrela(self, grafo: Graph, inicio, fim):
        """Busca A* (A-Star Search)"""
        self.nos_visitados = []
        self.arvore_busca = None
        
        if inicio == fim:
            return [inicio], NodeP(estado=inicio, v1=0, v2=0)
            
        # Fila de prioridade (deque com inserção ordenada)
        lista = deque()
        
        # v1 = f(n) = g(n) + h(n)
        h_inicial = self._heuristica_grafo(grafo, inicio, fim)
        raiz = NodeP(pai=None, estado=inicio, v1=h_inicial, v2=0)
        self.arvore_busca = raiz
        lista.append(raiz)
        
        # Controle de nós visitados/expandidos
        visitado = {inicio: raiz}
        
        while lista:
            # remove o nó com menor v1 (f(n))
            atual = lista.popleft()
            atual.expandido = True
            self.nos_visitados.append(atual.estado) # Adiciona o nó sendo expandido à ordem de visitação
            
            # Chegou ao objetivo
            if atual.estado == fim:
                caminho = self._reconstruir_caminho(atual)
                return caminho, self.arvore_busca, atual.v2
            
            # Gera sucessores
            vizinhos = grafo.obter_vizinhos(atual.estado)
            
            for vizinho, custo_aresta in vizinhos:
                # custo acumulado até o sucessor
                v2 = atual.v2 + custo_aresta
                # v1 = f(n) = g(n) + h(n)
                v1 = v2 + self._heuristica_grafo(grafo, vizinho, fim)
                
                # Não visitado ou custo melhor
                if (vizinho not in visitado) or (v2 < visitado[vizinho].v2):
                    filho = NodeP(pai=atual, estado=vizinho, v1=v1, v2=v2)
                    
                    # Atualiza o nó visitado
                    if vizinho in visitado:
                        try:
                            lista.remove(visitado[vizinho])
                        except ValueError:
                            pass
                    
                    visitado[vizinho] = filho
                    atual.adicionar_filho(filho)
                    self._inserir_ordenado(lista, filho)
                    
        return None, self.arvore_busca, 0

    # -----------------------------------------------------------------------------
    # AIA ESTRELA (Iterative Deepening A-Star - IDA*)
    # -----------------------------------------------------------------------------
    def aia_estrela(self, grafo: Graph, inicio, fim):
        """Busca A* com Aprofundamento Iterativo (IDA*)"""
        self.nos_visitados = []
        self.arvore_busca = None
        
        if inicio == fim:
            return [inicio], NodeP(estado=inicio, v1=0, v2=0)
            
        # Calcula o limite inicial (h(inicio))
        limite = self._heuristica_grafo(grafo, inicio, fim)
        
        while True:
            self.nos_visitados = []
            self.arvore_busca = None
            
            # Fila de prioridade (deque com inserção ordenada)
            lista = deque()
            
            # v1 = f(n) = g(n) + h(n)
            h_inicial = self._heuristica_grafo(grafo, inicio, fim)
            raiz = NodeP(pai=None, estado=inicio, v1=h_inicial, v2=0)
            self.arvore_busca = raiz
            lista.append(raiz)
            
            # Controle de nós visitados/expandidos
            visitado = {inicio: raiz}
            self.nos_visitados.append(inicio)
            
            proximo_limite = float('inf')
            
            while lista:
                # remove o nó com menor v1 (f(n))
                atual = lista.popleft()
                atual.expandido = True
                
                # Chegou ao objetivo
                if atual.estado == fim:
                    caminho = self._reconstruir_caminho(atual)
                    return caminho, self.arvore_busca, atual.v2
                
                # Gera sucessores
                vizinhos = grafo.obter_vizinhos(atual.estado)
                
                for vizinho, custo_aresta in vizinhos:
                    # custo acumulado até o sucessor
                    v2 = atual.v2 + custo_aresta
                    # v1 = f(n) = g(n) + h(n)
                    v1 = v2 + self._heuristica_grafo(grafo, vizinho, fim)
                    
                    if v1 > limite:
                        proximo_limite = min(proximo_limite, v1)
                        continue
                    
                    # Não visitado ou custo melhor
                    if (vizinho not in visitado) or (v2 < visitado[vizinho].v2):
                        filho = NodeP(pai=atual, estado=vizinho, v1=v1, v2=v2)
                        
                        # Atualiza o nó visitado
                        if vizinho in visitado:
                            try:
                                lista.remove(visitado[vizinho])
                            except ValueError:
                                pass
                        
                        visitado[vizinho] = filho
                        atual.adicionar_filho(filho)
                        self._inserir_ordenado(lista, filho)
                        self.nos_visitados.append(vizinho)
                        
            if proximo_limite == float('inf'):
                return None, self.arvore_busca, 0 # Caminho não encontrado
            
            limite = proximo_limite 