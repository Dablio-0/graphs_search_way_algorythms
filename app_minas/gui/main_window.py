#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QLabel, QLineEdit, QPushButton, 
                             QComboBox, QTextEdit, QFrame, QSplitter, QScrollArea,
                             QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QColor, QIntValidator
from .graph_viewer import GraphViewer
from .tree_viewer import TreeViewer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Otimização de Trajetos em Túneis de Mineração")
        self.setGeometry(100, 100, 1400, 900)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        
        # Painel esquerdo (controles)
        self.create_left_panel()
        
        # Painel direito (visualizações)
        self.create_right_panel()
        
        # Adicionar painéis ao layout principal
        main_layout.addWidget(self.left_panel, 1)
        main_layout.addWidget(self.right_panel, 3)
        
        # Aplicar estilo
        self.apply_styles()
        
    def create_left_panel(self):
        """Cria o painel esquerdo com os controles de entrada"""
        self.left_panel = QFrame()
        self.left_panel.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout(self.left_panel)
        
        # Título
        title = QLabel("CONTROLES DE BUSCA")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Campo Input Arquivo
        self.input_arquivo = QLineEdit()
        self.input_arquivo.setPlaceholderText("Caminho do arquivo do grafo...")
        layout.addWidget(self.input_arquivo)
        
        # Botão para carregar arquivo
        self.btn_carregar = QPushButton("Carregar Arquivo")
        layout.addWidget(self.btn_carregar)    
        
        # Label para Nomear o Campo Input Nó Origem
        layout.addWidget(QLabel("Nó Origem:"))

        # Campo Input Nó Origem
        self.input_origem = QLineEdit()
        self.input_origem.setPlaceholderText("Ex: 1")
        layout.addWidget(self.input_origem)

        # Label para Nomear o Campo Input Nó Destino
        layout.addWidget(QLabel("Nó Destino:"))

        # Campo Input Nó Destino
        self.input_destino = QLineEdit()
        self.input_destino.setPlaceholderText("Ex: 10")
        layout.addWidget(self.input_destino)
        
        # Campo Select Método
        self.combo_metodo = QComboBox()
        self.combo_metodo.addItems([
            "Busca em Amplitude",
            "Busca em Profundidade",
            "Busca em Profundidade Limitada",
            "Busca por Aprofundamento Iterativo",
            "Busca Bidirecional",
            "Custo Uniforme",
            "Greedy",
            "A-estrela",
            "AIA-estrela"
        ])
        layout.addWidget(self.combo_metodo)

        # Campo para limite de profundidade
        self.input_limite_profundidade = QLineEdit()
        self.input_limite_profundidade.setPlaceholderText("Limite de Profundidade (opcional)")
        self.input_limite_profundidade.setValidator(QIntValidator())
        self.input_limite_profundidade.setVisible(False) # Esconder por padrão
        layout.addWidget(self.input_limite_profundidade)

        self.combo_metodo.currentIndexChanged.connect(self.toggle_limite_profundidade_input)
        
        # Botão Executar
        self.btn_executar = QPushButton("EXECUTAR")
        self.btn_executar.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(self.btn_executar)
        
        # Área de texto para resultados
        self.text_resultado = QTextEdit()
        self.text_resultado.setMaximumHeight(200)
        self.text_resultado.setPlaceholderText("Os resultados da busca aparecerão aqui...")
        layout.addWidget(self.text_resultado)
        
        # Espaçamento flexível
        layout.addStretch()

    def toggle_limite_profundidade_input(self, index):
        metodo_selecionado = self.combo_metodo.itemText(index)
        if metodo_selecionado in ["Busca em Profundidade Limitada", "Busca por Aprofundamento Iterativo"]:
            self.input_limite_profundidade.setVisible(True)
        else:
            self.input_limite_profundidade.setVisible(False)
        
    from PyQt5.QtWidgets import QScrollArea

    def create_right_panel(self):
        """Cria o painel direito com as visualizações"""
        # Frame que vai conter tudo
        self.right_panel = QFrame()
        self.right_panel.setFrameStyle(QFrame.StyledPanel)
        right_layout = QVBoxLayout(self.right_panel)

        # Cria outro frame para colocar dentro do scroll
        content_frame = QFrame()
        content_layout = QVBoxLayout(content_frame)

        # --- Apresentação do Problema ---
        problema_frame = QFrame()
        problema_frame.setFrameStyle(QFrame.StyledPanel)
        problema_layout = QVBoxLayout(problema_frame)
        problema_label = QLabel("PROBLEMA: Otimização de Trajetos em Túneis de Mineração")
        problema_label.setWordWrap(True)
        problema_label.setAlignment(Qt.AlignCenter)
        problema_layout.addWidget(problema_label)
        
        descricao_label = QLabel(
            "1. Problema\n"
            "Encontrar trajetos eficientes em uma rede de túneis de mineração, minimizando custos (tempo, distância, energia etc.). "
            "Desafios: topologia complexa, restrições das máquinas, mudanças dinâmicas, múltiplos objetivos e segurança.\n\n"
            "2. Modelagem\n"
            "Grafo G = (V, E)\n"
            "V: nós (interseções, pontos de carga, bases)\n"
            "E: arestas com pesos que representam o custo de travessia\n"
            "Recomendação: usar lista de adjacência para redes esparsas.\n\n"
            "3. Estado\n"
            "Estado descrito por: nó atual, custo acumulado g(n) e caminho percorrido. Ex.: {'nó': 'A', 'custo': 0, 'caminho': ['A']}\n\n"
            "4. Sucessores\n"
            "Para um nó N, retornar [(sucessor, custo)] para cada nó adjacente.\n\n"
            "5. Custo\n"
            "Custo total = soma dos pesos das arestas ao longo do caminho; usado em UCS e A*.\n\n"
            "6. Heurística\n"
            "Estimativa do custo restante (ex.: distância euclidiana ou manhattan). Deve ser admissível (não superestimar) e, preferencialmente, consistente.\n\n"
            "Considerações práticas:\n"
            "- Respeitar restrições operacionais e condições dinâmicas.\n"
            "- Para múltiplos objetivos, combinar por pesos ou usar métodos multiobjetivo.\n"
            "- Atualizações online exigem replanejamento eficiente."
        )


        descricao_label.setWordWrap(True)
        descricao_label.setAlignment(Qt.AlignJustify)
        problema_layout.addWidget(descricao_label)
        content_layout.addWidget(problema_frame)

        # --- Visualização do Grafo ---
        graph_frame = QFrame()
        graph_frame.setFrameStyle(QFrame.StyledPanel)
        graph_layout = QVBoxLayout(graph_frame)
        graph_label = QLabel("VISUALIZAÇÃO DO GRAFO")
        graph_label.setAlignment(Qt.AlignCenter)
        graph_layout.addWidget(graph_label)
        self.graph_viewer = GraphViewer()
        graph_layout.addWidget(self.graph_viewer)
        content_layout.addWidget(graph_frame)
        self.graph_viewer.setMinimumSize(800, 400)

        # --- Visualização da Árvore ---
        tree_frame = QFrame()
        tree_frame.setFrameStyle(QFrame.StyledPanel)
        tree_layout = QVBoxLayout(tree_frame)
        tree_label = QLabel("ÁRVORE DE BUSCA")
        tree_label.setAlignment(Qt.AlignCenter)
        tree_layout.addWidget(tree_label)
        self.tree_viewer = TreeViewer()
        tree_layout.addWidget(self.tree_viewer)
        content_layout.addWidget(tree_frame)
        self.tree_viewer.setMinimumSize(800, 400)

        # --- Scroll Area ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(content_frame)

        # Adiciona scroll area ao layout do painel direito
        right_layout.addWidget(scroll_area)
        content_layout.addStretch()

        self.graph_viewer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tree_viewer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


        
    def apply_styles(self):
        """Aplica estilos à interface"""
        # Estilo geral
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QFrame {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 5px;
                margin: 5px;
                padding: 10px;
            }
            QLabel {
                font-weight: bold;
                color: #333;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 3px;
                font-size: 12px;
            }
            QTextEdit {
                border: 1px solid #ccc;
                border-radius: 3px;
                font-family: monospace;
            }
            QPushButton {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 3px;
                background-color: #e0e0e0;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        
    def get_input_values(self):
        """Retorna os valores dos campos de entrada"""
        return {
            'arquivo': self.input_arquivo.text(),
            'origem': self.input_origem.text(),
            'destino': self.input_destino.text(),
            'metodo': self.combo_metodo.currentText(),
            'limite_profundidade': self.input_limite_profundidade.text()
        }
        
    def set_resultado(self, texto):
        """Define o texto do resultado"""
        self.text_resultado.setText(texto)
        
    def get_graph_viewer(self):
        """Retorna o widget de visualização do grafo"""
        return self.graph_viewer
        
    def get_tree_viewer(self):
        """Retorna o widget de visualização da árvore"""
        return self.tree_viewer