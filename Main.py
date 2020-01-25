# -*- coding:utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

from GUI.MainGUI import MainGUI
from Kiwoom import Kiwoom

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Song's Trader")
        self.ui = MainGUI(self)
        # gui를 변수로 받고 중심위젯으로 해주는게 핵심이네..
        self.setCentralWidget(self.ui)
        self.check_time()
        #self.kiwoom = Kiwoom()
        #self.kiwoom.comm_connect()
        #self.check_state()

    def check_time(self):
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout)
        
        self.ui.status_bar.showMessage("a")
    
    def timeout(self):
        current_time = QTime.currentTime()
        text_time = current_time.toString("hh:mm:ss")
        self.time_msg = "현재시간: {}".format(text_time)
        self.ui.status_bar.showMessage(self.time_msg)

    def check_state(self):
        state = self.kiwoom.get_connect_state()
        if state == 1:
            self.state_msg = "서버 연결 중"
        else:
            self.state_msg = "서버 미 연결 중"

        self.ui.status_bar.showMessage(self.state_msg + " | " + self.time_msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    app.exec_()
