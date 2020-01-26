# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

class Selected(QWidget):
    Rows = 0
    def __init__(self, parent):
        super(Selected, self).__init__(parent)
        
        self.title = QLabel("자동 선정 종목 리스트", self)
        self.selected_labels = ["주문유형", "종목명", "호가구분", "수량", "가격", "상태"]
        self.selected_table = QTableWidget(self)
        self.selected_table.setRowCount(Selected.Rows)
        self.selected_table.setColumnCount(6)
        self.selected_table.setHorizontalHeaderLabels(self.selected_labels)
        
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.title, 0, 0, 1, 1)
        self.layout.addWidget(self.selected_table, 1, 0, 1, 5)

    @staticmethod
    def appendSelectedItem(self, itemLists):
        # all items should be str
        # itemLists = ["주문유형", "종목명", "호가구분", "수량", "가격", "상태"]
        self.selected_table.insertRow(Selected.Rows)
        for i in range(len(itemLists)):
            item = QTableWidgetItem(itemLists[i])
            item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.selected_table.setItem(Selected.Rows, i, item)
            self.selected_table.resizeRowsToContents()
        Selected.Rows += 1

        