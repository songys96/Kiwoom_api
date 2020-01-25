# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import  *
from PyQt5.QAxContainer import *

class Account(QWidget):
    accountRows = 0
    stockRows = 0
    def __init__(self, parent):
        super(Account, self).__init__(parent)
        self.adjustSize()
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

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.title, 0, 0, 1, 1)
        self.layout.addWidget(self.account_table, 1, 0, 1, 1)
        self.layout.addWidget(self.stock_table, 2, 0, 1, 1)

    def appendAccountItem(self, changes, total_buy, total_estimation, total_diff, total_profit, assets):
        # all item should be str
        items = []
        items.append(QTableWidgetItem(changes))
        items.append(QTableWidgetItem(total_buy))
        items.append(QTableWidgetItem(total_estimation))
        items.append(QTableWidgetItem(total_diff))
        items.append(QTableWidgetItem(total_profit))
        items.append(QTableWidgetItem(assets))
        self.account_table.insertRow(Account.accountRows)
        for i in range(len(items)):
            self.account_table.setItem(Account.accountRows, i, items[i])
        Account.accountRows += 1
            
    def appendStockItem(self, name, count, buy, current, estimate, profit):
        items = []
        items.append(QTableWidgetItem(name))
        items.append(QTableWidgetItem(count))
        items.append(QTableWidgetItem(buy))
        items.append(QTableWidgetItem(current))
        items.append(QTableWidgetItem(estimate))
        items.append(QTableWidgetItem(profit))
        self.stock_table.insertRow(Account.stockRows)
        for i in range(len(items)):
            self.stock_table.setItem(Account.stockRows, i, items[i])
        Account.stockRows += 1
        
