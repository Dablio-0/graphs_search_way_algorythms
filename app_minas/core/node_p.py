from .graph_model import Node

class NodeP(Node):
    """
    Classe para representar um nó na árvore de busca para algoritmos ponderados.
    Adiciona v1 (valor de avaliação f(n) = g(n) + h(n) ou h(n)) e v2 (custo acumulado g(n)).
    """
    def __init__(self, pai=None, estado=None, v1=0, v2=0):
        # A profundidade é calculada no construtor da classe base.
        profundidade = pai.profundidade + 1 if pai else 0
        # O custo (g(n)) é armazenado em 'custo' da classe base e em 'v2'.
        super().__init__(pai=pai, estado=estado, custo=v2, profundidade=profundidade)
        self.v1 = v1  # Valor de avaliação (f(n) ou h(n))
        self.v2 = v2  # Custo acumulado (g(n))
        
    def __lt__(self, other):
        """Define a comparação para ordenação em filas de prioridade (menor v1 primeiro)"""
        return self.v1 < other.v1

    def __repr__(self):
        return f"NodeP(estado={self.estado}, v1={self.v1}, v2={self.v2}, prof={self.profundidade})"