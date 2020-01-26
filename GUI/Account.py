# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

class Account(QWidget):
    accountRows = 0
    stockRows = 0
    def __init__(self, parent):
        super(Account, self).__init__(parent)
        
        self.setFixedWidth(700)

        self.title = QLabel("잔고 및 보유현황", self)
        self.account_labels = ["예수금(d+2)", "총매입", "총평가", "총손익", "총수익률", "추정자산"]
        self.account_table = QTableWidget(self)
        self.account_table.setRowCount(Account.accountRows)
        self.account_table.setColumnCount(6)
        self.account_table.setHorizontalHeaderLabels(self.account_labels)
        
        self.stock_labels = ["종목명", "보유량", "매입가", "현재가", "평가손익", "수익률"]
        self.stock_table = QTableWidget(self)
        self.stock_table.setRowCount(Account.stockRows)
        self.stock_table.setColumnCount(6)
        self.stock_table.setHorizontalHeaderLabels(self.stock_labels)

        self.realtime_check = QCheckBox("실시간 조회",self)
        self.load_btn = QPushButton("조회", self)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.title, 0, 0, 1, 1)
        self.layout.addWidget(self.account_table, 1, 0, 1, 5)
        self.layout.addWidget(self.stock_table, 2, 0, 3, 5)
        self.layout.addWidget(self.realtime_check, 5, 3, 1, 1)
        self.layout.addWidget(self.load_btn, 5, 4, 1, 1)

    # 사실상 필요없는 줄이지만 이용합시다. 한줄만 필요함......(계좌는 한개씩만 읽으니까...)
    @staticmethod
    def appendAccountItem(self, itemLists):
        # all item should be str
        # itemLists = ["예수금(d+2)", "총매입", "총평가", "총손익", "총수익률", "추정자산"]
        self.account_table.insertRow(Account.accountRows)
        for i in range(len(itemLists)):
            item = QTableWidgetItem(itemLists[i])
            item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.account_table.setItem(Account.accountRows, i, item)
        Account.accountRows += 1
            
    def appendStockItem(self, itemLists):
        #itemLists = ["종목명", "보유량", "매입가", "현재가", "평가손익", "수익률"]
        self.stock_table.insertRow(Account.stockRows)
        for i in range(len(itemLists)):
            item = QTableWidgetItem(itemLists[i])
            item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            self.stock_table.setItem(Account.stockRows, i, item)
        Account.stockRows += 1