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
        self.trade_stocks_done = False
        # 키움 인스턴스 생성
        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()
        self._init_events()
        

    def _init_events(self):
        self.check_timeout()
        self.load_buy_sell()
        self.check_time()
        self.setAccountInfo()
        self.check_balance()
        self.ui.order.item_edit.textChanged.connect(self.code_change)
        self.ui.order.order_btn.clicked.connect(self.send_order)
        self.ui.account.load_btn.clicked.connect(self.check_balance)

    def check_time(self):
        self.timer_time = QTimer(self)
        self.timer_time.start(1000)
        self.timer_time.timeout.connect(self.check_timeout)
        
        # 10초에 한번씩 보유현황 리로드
        self.timer_load = QTimer(self)
        self.timer_load.start(1000*10)
        if self.ui.account.realtime_check.isChecked():
            self.timer_load.timeout.connect(self.check_balance)
    
    def check_timeout(self):
        market_start_time = QTime(9, 0, 0)
        current_time = QTime.currentTime()

        #if current_time > market_start_time and self.trade_stocks_done is False:
        #    self.trade_stocks()
        #    self.trade_stocks_done = True

        text_time = current_time.toString("hh:mm:ss")
        self.time_msg = "현재시간: {}".format(text_time)
        self.ui.status_bar.showMessage(self.time_msg)
        self.check_state()

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

    # 잔고와 보유 현황을 로드하는 것.
    def check_balance(self):
        from GUI.Account import Account
        self.kiwoom.reset_opw00018_output()
        account_number = self.kiwoom.get_login_info("ACCNO")
        account_number = account_number.split(';')[0]
        print(account_number)

        # 기본정보 가져오기
        self.kiwoom.set_input_value("계좌번호", account_number)
        self.kiwoom.comm_rq_data("opw00018_req", "opw00018", 0, "0001")
        # 추가 정보 있을시 없을때까지 반복
        while self.kiwoom.remained_data:
            time.sleep(0.2)
            self.kiwoom.set_input_value("계좌번호", account_number)
            self.kiwoom.comm_rq_data("opw00018_req", "opw00018", 0, "2000")
        # 예수금은 따로 가져오기 
        self.kiwoom.set_input_value("계좌번호", account_number)
        self.kiwoom.comm_rq_data("opw00001_req", "opw00001", 0, "2000")
        # 계좌 테이블 채우기
        account_item_lists = [] # == ["예수금(d+2)", "총매입", "총평가", "총손익", "총수익률", "추정자산"]
        account_item_lists.append(self.kiwoom.d2_deposit)
        account_item_lists += self.kiwoom.opw00018_output['single']
        Account.appendAccountItem(self.ui.account, account_item_lists)
        
        # 보유주식현황 채우기
        stock_item_list = self.kiwoom.opw00018_output['multi']
        Account.appendStockItem(self.ui.account, stock_item_list)

    def load_buy_sell(self):        
        from GUI.Selected import Selected
        # 선정된 종목 채우기
        # it should be a method of cls
        f =  open("ex_buy_list.txt", "r", encoding="utf-8")
        buy_list = f.readlines()
        f.close()

        f =  open("ex_sell_list.txt", "r", encoding="utf-8")
        sell_list = f.readlines()
        f.close()

        for item_info in buy_list:
            item = item_info.split(';')
            #item[1] = self.kiwoom.get_master_code_name(item[1].rsplit())
            Selected.appendSelectedItem(self.ui.selected, item)
            
        for item_info in sell_list:
            item = item_info.split(';')
            #item[1] = self.kiwoom.get_master_code_name(item[1].rsplit())
            Selected.appendSelectedItem(self.ui.selected, item)

    # 선택된 종목 자동 주문시키기
    def trade_stocks(self):
        hoga_lookup = {"지정가": "00", "시장가": "03"}

        f = open("ex_sell_list.txt", "r", encoding="utf-8")
        sell_list = f.readlines()
        f.close()

        f = open("ex_buy_list.txt", "r", encoding="utf-8")
        buy_list = f.readlines()
        f.close()

        account = self.ui.order.account_combo.currentText()

        #buy list
        for row_data in buy_list:
            split_row_data = row_data.split(';')
            hoga = split_row_data[2]
            code = split_row_data[1]
            num = split_row_data[3]
            price = split_row_data[4]

            if split_row_data[-1].rstrip() == '매수전':
                self.kiwoom.send_order("send_order_req", "0101", account, 1, code, num, price, hoga_lookup[hoga], "")

        # sell list
        for row_data in sell_list:
            split_row_data = row_data.split(';')
            hoga = split_row_data[2]
            code = split_row_data[1]
            num = split_row_data[3]
            price = split_row_data[4]

            if split_row_data[-1].rstrip() == '매도전':
                self.kiwoom.send_order("send_order_req", "0101", account, 2, code, num, price, hoga_lookup[hoga], "")
        
        # buy list
        for i, row_data in enumerate(buy_list):
            buy_list[i] = buy_list[i].replace("매수전", "주문완료")

        # file update
        f = open("buy_list.txt", 'wt')
        for row_data in buy_list:
            f.write(row_data)
        f.close()

        # sell list
        for i, row_data in enumerate(sell_list):
            sell_list[i] = sell_list[i].replace("매도전", "주문완료")

        # file update
        f = open("sell_list.txt", 'wt')
        for row_data in sell_list:
            f.write(row_data)
        f.close()

    









if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    app.exec_()
