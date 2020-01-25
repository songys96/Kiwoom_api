# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5.QAxContainer import *

from .Order import Order

HELP = "https://doc.qt.io/qtforpython/PySide2/QtWidgets/index.html#module-PySide2.QtWidgets"

class MainGUI(QWidget):
    """
    각각의 특성에 맞는 GUI 모듈의 집합체 형식으로 만들었다.
    """
    def __init__(self):
        super().__init__()
        self.widget = QWidget()
        
        self.order = Order(self)

        self.status_bar = QStatusBar(self)
        self.status_bar.setFixedWidth(300)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.widget)
        self.repaint()
