# -*- coding:utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *

class LoginGUI(QMainWindow):
    def __init__(self):
        """
        버튼을 누를경우 로그인 창이 뜨는 다이얼로그
        gui의 변수만 언더바로 표기하였다
        """


        super().__init__()
        self.setWindowTitle("Song's Stocks")
        self.setGeometry(300, 300, 300, 150)

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        login_btn = QPushButton("Login", self)
        login_btn.move(20, 20)
        login_btn.clicked.connect(self.login)

        check_connection_btn = QPushButton("Check State", self)
        check_connection_btn.move(20, 70)
        check_connection_btn.clicked.connect(self.checkConnection)

    def login(self):
        ret = self.kiwoom.dynamicCall("CommConnect()")

    def checkConnection(self):
        if self.kiwoom.dynamicCall("GetConnectState()") == 0:
            self.statusBar().showMessage("Not Connected")
        else:
            self.statusBar().showMessage("Connected")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = LoginGUI()
    myWindow.show()
    app.exec_()

