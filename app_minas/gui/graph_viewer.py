#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QGraphicsView, QGraphicsScene, 
                             QGraphicsEllipseItem, QGraphicsLineItem, 
                             QGraphicsTextItem, QVBoxLayout, QScrollBar)
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.QtGui import QPen, QBrush, QColor, QFont, QPainter
import math

class GraphViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.graph_data = None
        self.path_nodes = []
        self.setup_ui()
        
    def setup_ui(self):
        """Configura a interface do visualizador de grafo"""
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
        
        # Sobrescreve o wheelEvent para zoom
        self.view.wheelEvent = self.wheelEvent
        
        layout.addWidget(self.view)
        
    def set_graph(self, nodes, edges, node_positions=None):
        """
        Define o grafo a ser visualizado
        
        Args:
            nodes: Lista de nós (ex: [1, 2, 3, 4, 5])
            edges: Lista de arestas com custos (ex: [(1, 2, 10), (2, 3, 15)])
            node_positions: Dicionário com posições dos nós (opcional)
        """
        self.graph_data = {
            'nodes': nodes,
            'edges': edges,
            'positions': node_positions or self.calculate_positions(nodes)
        }
        self.draw_graph()
        
    def calculate_positions(self, nodes):
        """Calcula posições automáticas para os nós em um layout circular"""
        positions = {}
        num_nodes = len(nodes)
        
        if num_nodes == 1:
            positions[nodes[0]] = (0, 0)
            return positions
            
        # Layout circular
        radius = 500
        center_x, center_y = 0, 0
        
        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / num_nodes
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            positions[node] = (x, y)
            
        return positions
        
    def draw_graph(self):
        """Desenha o grafo na cena"""
        if not self.graph_data:
            return
            
        self.scene.clear()
        
        nodes = self.graph_data['nodes']
        edges = self.graph_data['edges']
        positions = self.graph_data['positions']
        
        # Desenhar arestas primeiro
        for edge in edges:
            node1, node2 = edge[0], edge[1]
            if node1 in positions and node2 in positions:
                cost = edge[2]
                self.draw_edge(positions[node1], positions[node2], cost)
        
        # Desenhar nós
        for node in nodes:
            if node in positions:
                is_path_node = node in self.path_nodes
                self.draw_node(positions[node], str(node), is_path_node)
                
        # Ajustar a view para mostrar todo o grafo
        self.view.fitInView(self.scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        
    def draw_node(self, position, label, is_path_node=False):
        """Desenha um nó na posição especificada"""
        x, y = position
        radius = 35
        
        if is_path_node:
            brush = QBrush(QColor(255, 100, 100))
            pen = QPen(QColor(200, 0, 0), 3)
        else:
            brush = QBrush(QColor(200, 200, 255))
            pen = QPen(QColor(0, 0, 0), 2)
        
        circle = QGraphicsEllipseItem(x - radius, y - radius, 2 * radius, 2 * radius)
        circle.setBrush(brush)
        circle.setPen(pen)
        self.scene.addItem(circle)
        
        text = QGraphicsTextItem(label)
        text.setFont(QFont("Arial", 12, QFont.Bold))
        text.setPos(x - 10, y - 10)
        self.scene.addItem(text)
        
    def draw_edge(self, pos1, pos2, cost):
        """Desenha uma aresta entre duas posições e exibe o custo"""
        x1, y1 = pos1
        x2, y2 = pos2
        
        line = QGraphicsLineItem(x1, y1, x2, y2)
        line.setPen(QPen(QColor(0, 0, 0), 2))
        self.scene.addItem(line)
        
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx*dx + dy*dy)
        
        offset_dist = 20
        if length > 0:
            nx = -dy / length
            ny = dx / length
            offset_x = nx * offset_dist
            offset_y = ny * offset_dist
        else:
            offset_x = offset_y = 0
        
        text = QGraphicsTextItem(str(cost))
        text.setFont(QFont("Arial", 10))
        text.setDefaultTextColor(QColor(0, 0, 0))
        
        text_rect = text.boundingRect()
        text.setPos(mid_x - text_rect.width() / 2 + offset_x,
                    mid_y - text_rect.height() / 2 + offset_y)
        
        self.scene.addItem(text)
        
    def highlight_path(self, path):
        """Destaca o caminho encontrado"""
        self.path_nodes = path
        if self.graph_data:
            self.draw_graph()
            
    def wheelEvent(self, event):
        """Implementa a funcionalidade de zoom com a roda do mouse"""
        zoom_factor = 1.15
        if event.angleDelta().y() > 0:
            self.view.scale(zoom_factor, zoom_factor)
        else:
            self.view.scale(1.0 / zoom_factor, 1.0 / zoom_factor)
        event.accept()
            
    def clear_graph(self):
        """Limpa o grafo"""
        self.scene.clear()
        self.graph_data = None
        self.path_nodes = []
