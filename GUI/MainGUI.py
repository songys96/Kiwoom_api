# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5.QtCore import  *
from PyQt5.QAxContainer import *

from .Order import Order
from .Account import Account
from .Selected import Selected

HELP = "https://doc.qt.io/qtforpython/PySide2/QtWidgets/index.html#module-PySide2.QtWidgets"

class MainGUI(QWidget):
    """
    각각의 특성에 맞는 GUI 모듈의 집합체 형식으로 만들었다.
    """
    def __init__(self, parent):
        super(MainGUI, self).__init__(parent)
        self.setFixedSize(1000,650)
        self.order = Order(self)
        self.order.setFixedSize(200,270)
        self.account = Account(self)
        self.account.setFixedSize(700,300)
        self.selected = Selected(self)
        self.selected.setFixedSize(700,300)
        
        self.status_bar = QStatusBar(self)
        self.adjustSize()

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.order, 0, 0, 1, 1)
        self.layout.addWidget(self.account, 0, 1, 3, 2)
        self.layout.addWidget(self.selected, 3, 1, 1, 2)
        self.layout.addWidget(self.status_bar, 4, 0, 1, 1)

        
