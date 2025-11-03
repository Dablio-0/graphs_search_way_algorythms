#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QGraphicsView, QGraphicsScene, 
                             QGraphicsEllipseItem, QGraphicsLineItem, 
                             QGraphicsTextItem, QVBoxLayout)
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QFont, QPainter

class TreeViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.tree_data = None
        
    def setup_ui(self):
        """Configura a interface do visualizador de árvore"""
        layout = QVBoxLayout(self)
        
        # Cria a cena e a view
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setRenderHint(QPainter.TextAntialiasing)
        self.view.setRenderHint(QPainter.SmoothPixmapTransform)
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        self.view.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.view.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.view.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        
        layout.addWidget(self.view)
        
    def set_tree(self, root_node, search_type=""):
        """
        Define a árvore de busca a ser visualizada
        
        Args:
            root_node: Nó raiz da árvore de busca
            search_type: Tipo de busca realizada
        """
        self.tree_data = {
            'root': root_node,
            'search_type': search_type
        }
        self.draw_tree()
        
    def draw_tree(self):
        """Desenha a árvore de busca na cena"""
        if not self.tree_data or not self.tree_data['root']:
            return
            
        self.scene.clear()
        
        # Calcular posições dos nós na árvore
        positions = self.calculate_tree_positions(self.tree_data['root'])
        
        if not positions:
            return
            
        # Desenhar conexões primeiro
        self.draw_tree_connections(self.tree_data['root'], positions)
        
        # Desenhar nós
        self.draw_tree_nodes(self.tree_data['root'], positions)
        
        # Ajustar a view
        self.view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        
    def calculate_tree_positions(self, root):
        """Calcula as posições dos nós na árvore usando layout hierárquico"""
        positions = {}
        
        # Primeira passagem: calcular largura de cada subárvore
        def calculate_subtree_width(node):
            if not hasattr(node, 'filhos') or not node.filhos:
                return 1
            return max(1, sum(calculate_subtree_width(child) for child in node.filhos))
        
        # Segunda passagem: atribuir posições
        def assign_positions(node, x, y, available_width):
            positions[id(node)] = (x, y)
            
            if hasattr(node, 'filhos') and node.filhos:
                num_children = len(node.filhos)
                child_spacing = available_width / max(1, num_children)
                start_x = x - available_width/2 + child_spacing/2
                
                for i, child in enumerate(node.filhos):
                    child_x = start_x + i * child_spacing
                    child_width = calculate_subtree_width(child) * 60
                    assign_positions(child, child_x, y + 80, child_width)
        
        # Calcular largura total da árvore
        total_width = calculate_subtree_width(root) * 80
        
        # Atribuir posições começando da raiz
        assign_positions(root, 0, 0, total_width)
        
        return positions
        
    def draw_tree_nodes(self, root, positions):
        """Desenha os nós da árvore"""
        def draw_node_recursive(node):
            if id(node) not in positions:
                return
                
            x, y = positions[id(node)]
            
            # Desenhar nó
            radius = 25
            circle = QGraphicsEllipseItem(x - radius, y - radius, 2 * radius, 2 * radius)
            
            # Cor baseada no estado do nó
            if hasattr(node, 'objetivo') and node.objetivo:
                brush = QBrush(QColor(100, 255, 100))  # Verde para objetivo
                pen = QPen(QColor(0, 150, 0), 3)
            elif hasattr(node, 'expandido') and node.expandido:
                brush = QBrush(QColor(255, 200, 100))  # Laranja para expandido
                pen = QPen(QColor(200, 100, 0), 2)
            else:
                brush = QBrush(QColor(200, 200, 255))  # Azul para não expandido
                pen = QPen(QColor(0, 0, 150), 2)
                
            circle.setBrush(brush)
            circle.setPen(pen)
            self.scene.addItem(circle)
            
            # Rótulo do nó
            label = str(node.estado) if hasattr(node, 'estado') else "?"
            text = QGraphicsTextItem(label)
            text.setFont(QFont("Arial", 10, QFont.Bold))
            
            # Centralizar o texto
            text_rect = text.boundingRect()
            text.setPos(x - text_rect.width()/2, y - text_rect.height()/2)
            self.scene.addItem(text)
            
            # Desenhar filhos recursivamente
            if hasattr(node, 'filhos'):
                for child in node.filhos:
                    draw_node_recursive(child)
                    
        draw_node_recursive(root)
        
    def draw_tree_connections(self, root, positions):
        """Desenha as conexões entre os nós da árvore"""
        def draw_connections_recursive(node):
            if id(node) not in positions:
                return
                
            x1, y1 = positions[id(node)]
            
            if hasattr(node, 'filhos'):
                for child in node.filhos:
                    if id(child) in positions:
                        x2, y2 = positions[id(child)]
                        
                        # Linha de conexão
                        line = QGraphicsLineItem(x1, y1, x2, y2)
                        line.setPen(QPen(QColor(100, 100, 100), 2))
                        self.scene.addItem(line)
                        
                        # Continuar recursivamente
                        draw_connections_recursive(child)
                        
        draw_connections_recursive(root)
        
    def wheelEvent(self, event):
        """Implementa a funcionalidade de zoom com a roda do mouse"""
        zoom_factor = 1.15 # Fator de zoom
        
        if event.angleDelta().y() > 0:
            # Zoom in
            self.view.scale(zoom_factor, zoom_factor)
        else:
            # Zoom out
            self.view.scale(1.0 / zoom_factor, 1.0 / zoom_factor)
            
        event.accept()
        
    def clear_tree(self):
        """Limpa a árvore"""
        self.scene.clear()
        self.tree_data = None
        
    def set_search_info(self, info_text):
        """Adiciona informações sobre a busca"""
        # Adicionar texto informativo na parte superior
        text_item = QGraphicsTextItem(info_text)
        text_item.setFont(QFont("Arial", 12, QFont.Bold))
        text_item.setPos(-100, -50)
        text_item.setDefaultTextColor(QColor(50, 50, 50))
        self.scene.addItem(text_item)
