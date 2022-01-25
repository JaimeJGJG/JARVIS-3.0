#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  ListaC.py
#  
#  Copyright 2021 JaimeJG
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QMovie
from plyer import notification
from PyQt5.QtCore import QProcess
import sys

class JanelaC (QMainWindow):
	def __init__(self):
		super().__init__()
		
		self.label_JG = QLabel(self)
		self.label_JG.setText("LISTA DE COMANDOS")
		self.label_JG.setAlignment(QtCore.Qt.AlignRight)
		self.label_JG.move(5,5)
		self.label_JG.setStyleSheet('QLabel {font-size:18px;color:#0000FF;font:bold}')
		self.label_JG.resize(195,20)
		
		ListaC = QListWidget(self)
		ListaC.setGeometry(5, 30, 290, 370)
		#ListaC.setStyleSheet('background-color:black;color:blue')
		ListaC.setStyleSheet("""
		QListWidget::item{
            color:blue;
            background-color:transparent;}
            
		QScrollBar:vertical{       
            border:none;
            background:black;
            width:3px;
            margin:0px;}
            
        QScrollBar::handle:vertical{
            background:blue;
            min-height:0px;}
            
        QScrollBar::add-line:vertical{
            background:black;
            height: 0px;
            subcontrol-position:bottom;
            subcontrol-origin:margin;}
            
        QScrollBar::sub-line:vertical{
            background:black;
            height:0px;
            subcontrol-position:top;
            subcontrol-origin:margin;}
        """)
        

		ls = ['Olá', 'Tudo Bem', 'Bom dia', 'Boa tarde', 'Boa noite', 'Que horas',
		'Qual é a data','Como está o clima?', 'Tocar música', 'Proxima música', 'Música anterior',
		'Aumentar volume', 'Diminua o volume', 'Pausa reprodução', 'Continue a reproduzir',
		'Abrir Google', 'Abrir Youtube', 'Meus arquivos', 'Iniciar pesquisa', 'Me fale sobre um assunto',
		'Fique em silêncio', 'Carga da bateria', 'Carga do sistema', 'Temperatura da CPU']
		ListaC.addItems(ls)

		botao_fechar = QPushButton("",self)
		botao_fechar.move(270,5)
		botao_fechar.resize(20,20)
		botao_fechar.setStyleSheet("background-image : url(FECHAR.png);border-radius: 15px;") 
		botao_fechar.clicked.connect(self.fechartudo)
			
		self.CarregarJanela()
		
	def CarregarJanela(self):
		self.setWindowFlag(Qt.FramelessWindowHint)
		self.setGeometry(50,50,300,410)
		self.setMinimumSize(300, 410)
		self.setMaximumSize(300, 410)
		self.setWindowOpacity(0.95) 
		#self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.setStyleSheet("background-color: black")
		self.setWindowIcon(QtGui.QIcon('ICONE.png'))
		self.setWindowTitle("COMANDOS")
		self.show()
	
	def fechartudo(self):
		print('botao fechar presionado')
		sys.exit()
	
	def mousePressEvent(self, event):
		if event.buttons() == Qt.LeftButton:
			self.dragPos = event.globalPos()
			event.accept()
    
	def mouseMoveEvent(self, event):
		if event.buttons() == Qt.LeftButton:
			self.move(self.pos() + event.globalPos() - self.dragPos)
			self.dragPos = event.globalPos()
			event.accept()
	
aplicacao = QApplication(sys.argv)
j = JanelaC()
sys.exit(aplicacao.exec_())
