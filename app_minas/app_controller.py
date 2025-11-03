#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from core.graph_model import Graph
from core.search_algorithms import SearchAlgorithms
from core.search_algorithms_p import SearchAlgorithmsP
from core.node_p import NodeP
from core.utils import validar_entrada, calcular_custo_caminho, formatar_resultado

class SearchWorker(QThread):
    """Worker thread para executar algoritmos de busca sem travar a interface"""
    finished = pyqtSignal(list, object, str)  # caminho, arvore, resultado_texto
    error = pyqtSignal(str)
    
    def __init__(self, grafo, origem, destino, algoritmo, limite_profundidade=None):
        super().__init__()
        self.grafo = grafo
        self.origem = origem
        self.destino = destino
        self.algoritmo = algoritmo
        self.limite_profundidade = limite_profundidade
        
    def run(self):
        try:
            search = SearchAlgorithms()
            search_p = SearchAlgorithmsP()
            caminho = None
            arvore = None
            
            if self.algoritmo == "Busca em Amplitude":
                caminho, arvore = search.busca_amplitude(self.grafo, self.origem, self.destino)
                custo = calcular_custo_caminho(self.grafo, caminho) if caminho else 0
            elif self.algoritmo == "Busca em Profundidade":
                caminho, arvore = search.busca_profundidade(self.grafo, self.origem, self.destino)
                custo = calcular_custo_caminho(self.grafo, caminho) if caminho else 0
            elif self.algoritmo == "Busca em Profundidade Limitada":
                limite = self.limite_profundidade if self.limite_profundidade is not None else 5
                caminho, arvore = search.busca_profundidade_limitada(self.grafo, self.origem, self.destino, limite)
                custo = calcular_custo_caminho(self.grafo, caminho) if caminho else 0
            elif self.algoritmo == "Busca por Aprofundamento Iterativo":
                limite_inicial = self.limite_profundidade if self.limite_profundidade is not None else 1
                caminho, arvore = search.busca_aprofundamento_iterativo(self.grafo, self.origem, self.destino, limite_inicial)
                custo = calcular_custo_caminho(self.grafo, caminho) if caminho else 0
            elif self.algoritmo == "Busca Bidirecional":
                caminho, arvore = search.busca_bidirecional(self.grafo, self.origem, self.destino)
                custo = calcular_custo_caminho(self.grafo, caminho) if caminho else 0
            elif self.algoritmo == "Custo Uniforme":
                caminho, arvore, custo = search_p.custo_uniforme(self.grafo, self.origem, self.destino)
            elif self.algoritmo == "Greedy":
                caminho, arvore, custo = search_p.greedy(self.grafo, self.origem, self.destino)
            elif self.algoritmo == "A-estrela":
                caminho, arvore, custo = search_p.a_estrela(self.grafo, self.origem, self.destino)
            elif self.algoritmo == "AIA-estrela":
                caminho, arvore, custo = search_p.aia_estrela(self.grafo, self.origem, self.destino)
            else:
                caminho, arvore = None, None
                custo = 0

            # Determinar qual lista de nós visitados usar
            if self.algoritmo in ["Custo Uniforme", "Greedy", "A-estrela", "AIA-estrela"]:
                nos_visitados = search_p.nos_visitados
            else:
                nos_visitados = search.nos_visitados

            # Formatar resultado
            resultado_texto = formatar_resultado(
                caminho, custo, self.algoritmo, nos_visitados
            )

            self.finished.emit(caminho or [], arvore, resultado_texto)
            
        except Exception as e:
            self.error.emit(f"Erro durante a busca: {str(e)}")


class AppController:
    """Controlador principal da aplicação"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.grafo = Graph()
        self.search_worker = None
        
        # Conectar sinais
        self.conectar_sinais()
        
    def conectar_sinais(self):
        """Conecta os sinais da interface com os métodos do controlador"""
        self.main_window.btn_carregar.clicked.connect(self.carregar_arquivo)
        self.main_window.btn_executar.clicked.connect(self.executar_busca)
        
    def carregar_arquivo(self):
        """Carrega um arquivo de grafo"""
        arquivo, _ = QFileDialog.getOpenFileName(
            self.main_window,
            "Carregar Arquivo de Grafo",
            "",
            "Arquivos de Texto (*.txt);;Todos os Arquivos (*)"
        )
        
        if arquivo:
            if self.grafo.carregar_de_arquivo(arquivo):
                self.main_window.input_arquivo.setText(arquivo)
                self.atualizar_visualizacao_grafo()
                QMessageBox.information(
                    self.main_window,
                    "Sucesso",
                    f"Grafo carregado com sucesso!\nNós: {len(self.grafo.nos)}"
                )
            else:
                QMessageBox.warning(
                    self.main_window,
                    "Erro",
                    "Erro ao carregar o arquivo. Verifique o formato."
                )
        
    def executar_busca(self):
        """Executa o algoritmo de busca selecionado"""
        valores = self.main_window.get_input_values()
        
        # Validar entrada
        valido, resultado = validar_entrada(
            valores['origem'], 
            valores['destino'], 
            self.grafo.nos
        )
        
        if not valido:
            QMessageBox.warning(self.main_window, "Erro de Validação", resultado)
            return
            
        origem, destino = resultado
        algoritmo = valores['metodo']
        limite_profundidade_str = valores['limite_profundidade']
        limite_profundidade = int(limite_profundidade_str) if limite_profundidade_str else None
        
        # Limpar resultados anteriores
        self.main_window.set_resultado("Executando busca...")
        self.main_window.get_graph_viewer().highlight_path([])
        self.main_window.get_tree_viewer().clear_tree()
        
        # Executar busca em thread separada
        self.search_worker = SearchWorker(self.grafo, origem, destino, algoritmo, limite_profundidade)
        self.search_worker.finished.connect(self.on_busca_concluida)
        self.search_worker.error.connect(self.on_busca_erro)
        self.search_worker.start()
        
    def on_busca_concluida(self, caminho, arvore, resultado_texto):
        """Callback quando a busca é concluída"""
        self.main_window.set_resultado(resultado_texto)
        
        if caminho:
            self.main_window.get_graph_viewer().highlight_path(caminho)
            
        if arvore:
            self.main_window.get_tree_viewer().set_tree(arvore)
            
    def on_busca_erro(self, erro):
        """Callback quando ocorre erro na busca"""
        QMessageBox.critical(self.main_window, "Erro na Busca", erro)
        self.main_window.set_resultado(f"Erro: {erro}")
        
    def atualizar_visualizacao_grafo(self):
        """Atualiza a visualização do grafo"""
        dados = self.grafo.obter_dados_visualizacao()
        self.main_window.get_graph_viewer().set_graph(
            dados['nos'],
            dados['arestas'],
            dados['posicoes']
        )
