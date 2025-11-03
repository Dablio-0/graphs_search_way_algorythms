#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicação Desktop para Otimização de Trajetos em Túneis de Mineração
Autor: Sistema de IA
Data: 2025
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from app_controller import AppController

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Otimização de Trajetos em Minas")
    app.setApplicationVersion("1.0")
    
    window = MainWindow()
    controller = AppController(window)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

