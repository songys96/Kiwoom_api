# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5.QAxContainer import *

class Order(QWidget):
    """
    각각의 특성에 맞는 GUI 모듈의 집합체 형식으로 만들었다.
    """
    def __init__(self, parent):
        super(Order, self).__init__(parent)

        self.title = QLabel("수동주문", self)
        self.account_label = QLabel("계좌", self)
        self.account_combo = QComboBox(self)
        self.order_label = QLabel("주문", self)
        self.order_combo = QComboBox(self)
        self.order_combo.addItems(["신규매수", "신규매도", "매수취소", "매도취소"])
        self.item_label = QLabel("종목", self)
        self.item_edit = QLineEdit(self)
        self.item_code_edit = QLineEdit(self)
        self.kind_label = QLabel("종류", self)
        self.kind_combo = QComboBox(self)
        self.kind_combo.addItems(["지정가", "시장가"])
        self.count_label = QLabel("수량", self)
        self.count_spin = QSpinBox(self)
        self.count_spin.setMinimum(0)
        self.price_label = QLabel("가격", self)
        self.price_spin = QSpinBox(self)
        self.price_spin.setMinimum(0)

        self.order_btn = QPushButton("현금주문", self)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.title, 0, 0, 1, 1)
        self.layout.addWidget(self.account_label, 1, 0, 1, 1)
        self.layout.addWidget(self.account_combo, 1, 1, 1, 3)
        self.layout.addWidget(self.order_label, 2, 0, 1, 1)
        self.layout.addWidget(self.order_combo, 2, 1, 1, 3)
        self.layout.addWidget(self.item_label, 3, 0, 1, 1)
        self.layout.addWidget(self.item_edit, 3, 1, 1, 3)
        self.layout.addWidget(self.item_code_edit, 4, 1, 1, 3)
        self.layout.addWidget(self.kind_label, 5, 0, 1, 1)
        self.layout.addWidget(self.kind_combo, 5, 1, 1, 3)
        self.layout.addWidget(self.count_label, 6, 0, 1, 1)
        self.layout.addWidget(self.count_spin, 6, 1, 1, 3)
        self.layout.addWidget(self.price_label, 7, 0, 1, 1)
        self.layout.addWidget(self.price_spin, 7, 1, 1, 3)
        self.layout.addWidget(self.order_btn, 8, 0, 1, 2)
        
