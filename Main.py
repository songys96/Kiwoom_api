# -*- coding:utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

from GUI.MainGUI import MainGUI
from Kiwoom import Kiwoom
from utils import change_money_format

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Song's Trader")
        self.ui = MainGUI(self)
        self.setCentralWidget(self.ui) # gui를 변수로 받고 중심위젯으로 해주는게 핵심이네..
        
        # 키움 인스턴스 생성
        #self.kiwoom = Kiwoom()
        #self.kiwoom.comm_connect()
        #self.check_state()
        self._init_events()

    def _init_events(self):
        self.check_time()
        #self.setAccountInfo()
        self.ui.order.item_edit.textChanged.connect(self.code_change)
        self.ui.order.order_btn.clicked.connect(self.send_order)
        self.ui.account.load_btn.clicked.connect(self.check_balance)

    def check_time(self):
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.timeout)
    
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

    def setAccountInfo(self):
        account_num = int(self.kiwoom.get_login_info("ACCOUNT_CNT"))
        accounts = self.kiwoom.get_login_info("ACCNO")
        account_list = accounts.split(";")[0:account_num]
        self.ui.order.account_combo.addItems(account_list)
        
    def code_change(self):
        # price(현재가) 축가하는 메서드 넣어야할듯
        code = self.ui.order.item_edit.text()
        name = self.kiwoom.get_master_code_name(code)
        self.ui.order.item_code_edit.setText(name)

    def send_order(self):
        order_type_lookup = {"신규매수": 1, "신규매도": 2, "매수취소": 3, "매도취소": 4}
        hoga_lookup = {"지정가": "00", "시장가": "03"}

        account = self.ui.order.account_combo.currentText()
        order_type = self.ui.order.order_type_combo.currentText()
        code = self.ui.order.item_code_edit.text()
        hoga = self.ui.order.kind_combo.currentText()
        num = self.ui.order.count_spin.value()
        price = self.ui.order.price_spin.value()

        self.kiwoom.send_order("send_order_req", "0101", account, order_type_lookup[order_type],\
            code, num, price, hoga_lookup[hoga], "")

    def check_balance(self):
        from GUI.Account import Account

        self.kiwoom.reset_opw00018_output()
        account_number = self.kiwoom.get_login_info("ACCNO")
        account_number = account_number.split(';')[0]

        # 기본정보 가져오기
        self.kiwoom.set_input_value("계좌번호", account_number)
        self.kiwoom.comm_rq_data("opw00018_req", "opw00018", 2, "2000")
        # 추가 정보 있을시 없을때까지 반복
        while self.kiwoom.remained_data:
            time.sleep(0.2)
            self.kiwoom.set_input_value("계좌번호", account_number)
            self.kiwoom.comm_rq_data("opw00018_req", "opw00018", 2, "2000")
        # 예수금은 따로 가져오기
        self.kiwoom.set_input_value("계좌번호", account_number)
        self.kiwoom.comm_rq_data("opw00001_req", "opw00001", 0, "2000")
        
        itemLists = [] # == ["예수금(d+2)", "총매입", "총평가", "총손익", "총수익률", "추정자산"]
        itemLists.append(self.kiwoom.d2_deposit)
        itemLists += self.kiwoom.opw00018_output['single']
        Account.appendAccountItem(self.ui.account, itemLists)


        

    









if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    app.exec_()
