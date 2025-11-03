#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de teste em modo console para verificar os algoritmos de busca
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.graph_model import Graph
from core.search_algorithms import SearchAlgorithms
from core.utils import calcular_custo_caminho, formatar_resultado

def testar_algoritmos(caminho_arquivo_grafo):
    """Testa todos os algoritmos de busca"""
    print("=== TESTE DOS ALGORITMOS DE BUSCA ===\n")
    
    # Carregar grafo de exemplo
    grafo = Graph()
    # Para testes de algoritmo, carregamos o grafo do arquivo de teste
    grafo.carregar_de_arquivo(caminho_arquivo_grafo)
    
    print(f"Grafo carregado: {len(grafo.nos)} nós")
    print(f"Nós disponíveis: {grafo.nos}")
    print()
    
    # Definir origem e destino para teste
    origem = 1
    destino = 10
    
    print(f"Testando busca de {origem} para {destino}\n")
    
    # Instanciar algoritmos
    search = SearchAlgorithms()
    
    # Lista de algoritmos para testar
    algoritmos = [
        ("Busca em Amplitude", lambda: search.busca_amplitude(grafo, origem, destino)),
        ("Busca em Profundidade", lambda: search.busca_profundidade(grafo, origem, destino)),
        ("Busca em Profundidade Limitada", lambda: search.busca_profundidade_limitada(grafo, origem, destino, 5)),
        ("Busca por Aprofundamento Iterativo", lambda: search.busca_aprofundamento_iterativo(grafo, origem, destino, 1)), # Limite inicial 1 para teste
        ("Busca Bidirecional", lambda: search.busca_bidirecional(grafo, origem, destino))
    ]
    
    # Testar cada algoritmo
    for nome_algoritmo, funcao_busca in algoritmos:
        print(f"--- {nome_algoritmo} ---")
        try:
            caminho, arvore = funcao_busca()
            
            if caminho:
                custo = calcular_custo_caminho(grafo, caminho)
                resultado = formatar_resultado(caminho, custo, nome_algoritmo, search.nos_visitados)
                print(resultado)
                
                # Informações sobre a árvore
                if arvore:
                    print(f"Árvore de busca criada com raiz: {arvore.estado}")
                    print(f"Nó objetivo encontrado: {arvore.objetivo if hasattr(arvore, 'objetivo') else 'N/A'}")
            else:
                print("Caminho não encontrado")
                
        except Exception as e:
            print(f"Erro: {e}")
            
        print("-" * 50)
        print()

def testar_carregamento_arquivo():
    """Testa o carregamento de arquivo"""
    print("=== TESTE DE CARREGAMENTO DE ARQUIVO ===\n")
    
    # Criar arquivo de exemplo
    conteudo_arquivo = """10
1 2 20
1 5 20
1 6 5
1 7 15
2 3 15
2 8 20
2 10 15
3 4 5
3 10 5
4 5 10
4 10 10
5 6 5
6 7 10
7 8 5
8 9 20
9 10 10"""
    
    with open("teste_grafo.txt", "w") as arquivo:
        arquivo.write(conteudo_arquivo)
    
    # Testar carregamento
    grafo = Graph()
    sucesso = grafo.carregar_de_arquivo("teste_grafo.txt")
    
    if sucesso:
        print("Arquivo carregado com sucesso!")
        print(f"Nós: {grafo.nos}")
        print(f"Arestas por nó:")
        for no in grafo.nos:
            vizinhos = grafo.obter_vizinhos(no)
            print(f"  {no}: {vizinhos}")
    else:
        print("Erro ao carregar arquivo")
    
    # Limpar arquivo de teste
    os.remove("teste_grafo.txt")
    print()

def main():
    """Função principal"""
    print("Iniciando testes da aplicação de otimização de trajetos em minas...\n")
    
    # Testar carregamento de arquivo
    testar_carregamento_arquivo()
    
    # Criar arquivo de teste para os algoritmos (sem custos)
    grafo_teste_algoritmos_path = "teste_grafo_algoritmos.txt"
    conteudo_arquivo_algoritmos = """10
1 2
1 5
1 6
1 7
2 3
2 8
2 10
3 4
3 10
4 5
4 10
5 6
6 7
7 8
8 9
9 10"""
    with open(grafo_teste_algoritmos_path, "w") as arquivo:
        arquivo.write(conteudo_arquivo_algoritmos)

    # Testar algoritmos
    testar_algoritmos(grafo_teste_algoritmos_path)

    # Limpar arquivo de teste
    os.remove(grafo_teste_algoritmos_path)


    
    print("Testes concluídos!")

if __name__ == "__main__":
    main()

