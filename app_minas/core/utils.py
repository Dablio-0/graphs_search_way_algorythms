#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def calcular_custo_caminho(grafo, caminho):
    """Calcula o custo total de um caminho"""
    if not caminho or len(caminho) < 2:
        return 0
        
    custo_total = 0
    for i in range(len(caminho) - 1):
        custo_aresta = grafo.obter_custo_aresta(caminho[i], caminho[i + 1])
        if custo_aresta == float('inf'):
            return float('inf')  # Caminho inválido
        custo_total += custo_aresta
        
    return custo_total

def validar_entrada(origem, destino, nos_grafo):
    """Valida se os nós de origem e destino existem no grafo"""
    try:
        origem_int = int(origem)
        destino_int = int(destino)
        
        if origem_int not in nos_grafo:
            return False, f"Nó de origem {origem_int} não existe no grafo"
            
        if destino_int not in nos_grafo:
            return False, f"Nó de destino {destino_int} não existe no grafo"
            
        return True, (origem_int, destino_int)
        
    except ValueError:
        return False, "Origem e destino devem ser números inteiros"

def formatar_resultado(caminho, custo, algoritmo, nos_visitados):
    """Formata o resultado da busca para exibição"""
    if not caminho:
        return f"Algoritmo: {algoritmo}\nResultado: Caminho não encontrado"
        
    resultado = f"Algoritmo: {algoritmo}\n"
    resultado += f"Caminho encontrado: {' → '.join(map(str, caminho))}\n"
    resultado += f"Custo total: {custo}\n"
    resultado += f"Número de nós no caminho: {len(caminho)}\n"
    resultado += f"Nós visitados: {len(nos_visitados)}\n"
    resultado += f"Ordem de visitação: {' → '.join(map(str, nos_visitados))}"
    
    return resultado

def criar_arquivo_exemplo():
    """Cria um arquivo de exemplo para teste"""
    conteudo = """10
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
    
    with open("exemplo_grafo.txt", "w") as arquivo:
        arquivo.write(conteudo)
        
    return "exemplo_grafo.txt"

