# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

from utils import change_money_format, change_percentage_format


class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

    # 인스턴스 생성시 필수조건
    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    # 서버에 연결시 메서드 실행 슬롯(이벤트) 지정
    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveChejanData.connect(self._receive_chejan_data)

    # 메서드 실행시 서버에 연결
    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        # 아래 항목은 GUI가 아닐 경우에 사용 
        # ***PyQt에는 이벤트루프가 이미 있음
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    # 연결상태를 확인하는 메서드
    def _event_connect(self, err_code):
        self.login_event_loop.exit()

        if err_code == 0:
            print("connected")
        else: 
            print("disconnected")

        self.login_event_loop.exit()
    
    # 시장에서 코드 리스트 가져오는 메서드
    """
    market값에는 0:장내 3:ELW 4:뮤추얼펀드 5:신주인수권
                6:리츠 8:ETF 9:하이일드펀드 10:코스닥 30:제3시장
    """
    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GGetCodeListByMarket(QString)", market)
        code_list = code_list.split(";")
        return code_list[:-1]

    # ?
    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    # 현재상태 출력
    def get_connect_state(self):
        ret = self.dynamicCall("GetConnectState()")
        return ret

    # 찾고자 하는 정보를 입력한다
    # id : 종목코드, 계좌번호등 value:000660, 5015123401...
    # 하나의 대상에 대해 여러가지 필터로 찾는것 같음..
    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    # 요청하기
    # input(rqname:사용자구분명, trcode:Tran명, next:0-조회, 2-연속, screen_no:4자리화면번호)
    def comm_rq_data(self, rqname, trcode, next, screen_no):
        # 이부분 닫는거 좀 이상함 17-3-2 일봉데이터연속조회 부분
        self.dynamicCall("CommRqData(QString, QString, int, QString)",rqname, trcode, next, screen_no)
        # ***PyQt에는 이벤트루프가 이미 있음
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    # TR처리에 대한 이벤트 발생시 실제로 데이터를 가져오는 메서드
    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString)", code,
        real_type, field_name, index, item_name)
        return ret.strip()

    # 총 몇개의 데이터가 왔는지 확인
    # rqcode = requestcode 확인하고자 하는 정보코드의 요청을 보낸다
    # opt10001 : 주식기본정보 요청
    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, Qstring)", trcode, rqname)
        return ret

    # tr은 서버로부터 데이터를 주고받는 행위
    def _receive_tr_data(self, screen_no, rqname, record_name, next, unused1, unused2, unused3, unused4):
        if next == "2":
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10081_req":
            self._opt10081(rqname, trcode)
        elif rqname == "opw00001_req":
            self._opw00001(rqname, trcode)
        elif rqname == "opw00018_req":
            self._opw00018(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError():
            pass

    # 요청한 주식의 정보얻는 코드
    def _opt10081(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)

        for i in range(data_cnt):
            date = self._comm_get_data(trcode, "", rqname, i, "일자")
            open = self._comm_get_data(trcode, "", rqname, i, "시가")
            high = self._comm_get_data(trcode, "", rqname, i, "고가")
            low = self._comm_get_data(trcode, "", rqname, i, "저가")
            close = self._comm_get_data(trcode, "", rqname, i, "현재가")
            volume = self._comm_get_data(trcode, "", rqname, i, "거래량")
            
            self.ohlcv['date'].append(date)
            self.ohlcv['open'].append(int(open))
            self.ohlcv['high'].append(int(high))
            self.ohlcv['low'].append(int(low))
            self.ohlcv['close'].append(int(close))
            self.ohlcv['volume'].append(int(volume))

    # 요청한 추정예수금 정보 얻는 코드
    def _opw00001(self, rqname, trcode):
        d2_deposit = self._comm_get_data(trcode, "", rqname, 0, "d+2추정예수금")
        self.d2_deposit = change_money_format(d2_deposit)
      
    def reset_opw00018_output(self):
        self.opw00018_output = {'single': [], 'multi':[]}

    # 여기에서 single 의 경우 계좌의 잔고(위에 있는 한 줄)를 가져올 수 있음
    # multi의 경우 상세한 보유 현황을 가져 올것임
    def _opw00018(self, rqname, trcode):
        # single - 계좌의 정보
        total_purchase_price = self._comm_get_data(trcode, "", rqname, 0, "총매입금액")
        total_eval_price = self._comm_get_data(trcode, "", rqname, 0, "총평가금액")
        total_eval_profit_loss_price = self._comm_get_data(trcode, "", rqname, 0, "총평가손익금액")
        # 서버에 따라 달라질 수 있다 get_server_gubun()실행
        total_earning_rate = self._comm_get_data(trcode, "", rqname, 0, "총수익률(%)")
        estimated_deposit = self._comm_get_data(trcode, "", rqname, 0, "추정예탁자산")

        self.opw00018_output['single'].append(change_money_format(total_purchase_price))
        self.opw00018_output['single'].append(change_money_format(total_eval_price))
        self.opw00018_output['single'].append(change_money_format(total_eval_profit_loss_price))
        if self.get_server_gubun():
            total_earning_rate = float(total_earning_rate) / 100
            total_earning_rate = str(total_earning_rate)
        self.opw00018_output['single'].append(total_earning_rate)
        self.opw00018_output['single'].append(change_money_format(estimated_deposit))


        rows = self._get_repeat_cnt(trcode, rqname)
        for i in rows:
            name = self._comm_get_data(trcode, "", rqname, i, "종목명")
            quantity = self._comm_get_data(trcode, "", rqname, i, "보유수량")
            purchase_price = self._comm_get_data(trcode, "", rqname, i, "매입가")
            current_price = self._comm_get_data(trcode, "", rqname, i, "현재가")
            eval_profit_loss_price = self._comm_get_data(trcode, "", rqname, i, "평가손익")
            earning_rate = self._comm_get_data(trcode, "", rqname, i, "수익률(%)")

            quantity = change_money_format(quantity)
            purchase_price = change_money_format(purchase_price)
            current_price = change_money_format(current_price)
            eval_profit_loss_price = change_money_format(eval_profit_loss_price)
            earning_rate = change_percentage_format(earning_rate)

            self.opw00018_output['multi'].append([name, quantity, purchase_price, current_price, eval_profit_loss_price, earning_rate])

    def get_server_gubun(self):
        ret = self.dynamicCall("KOA_Functions(QString, QString)", "GetServerGubun", "")
        return ret


    # 주문하는 메서드 1번
    # 이벤트루프로 기다려줘야함
    def send_order(self, rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no):
        self.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, int, QString, QString)",\
            [rqname, screen_no, acc_no, order_type, code, quantity, price, hoga, order_no])

    # 체결잔고 데이터를 가져오는 메서드 3번
    def get_chejan_data(self, fid):
        ret = self.dynamicCall("GetChejanData(int)", fid)
        return ret

    # 체결데이터 확인 2번
    def _receive_chejan_data(self, gubun, item_cnt, fid_list):
        # 904:원주문번호 905:주문구분 908:체결시간 909:체결번호 910:체결가 911:체결량 10:현재가
        print(gubun)
        print(self.get_chejan_data(9203)) # 주문번호
        print(self.get_chejan_data(302)) # 종목명
        print(self.get_chejan_data(900)) # 주문수량
        print(self.get_chejan_data(901)) # 미체결수량

    # 본인의 계좌 정보 가져오기
    def get_login_info(self, tag):
        ret = self.dynamicCall("GetLoginInfo(QString)", tag)
        return ret
 


"""
# 여기는 단일 실행시 필요 -> 일봉 데이터 받는 법
if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
     kiwoom.comm_connect()

    kiwoom.ohlcv = {'data':[], 'open':[], 'high':[], 'low':[], 'close':[], 'volume':[]}
    
    kiwoom.set_input_value("종목코드", "039490")
    kiwoom.set_input_value("기준일자", "20170224")
    kiwoom.set_input_value("수정주가구분", 1)
    kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "0101")

    while kiwoom.remained_data == True:
        # 1초에 5번의 TR만 요청가능 하므로 좀 쉬엄쉬엄 하자
        time.sleep(TR_REQ_TIME_INTERVAL)
        kiwoom.set_input_value("종목코드", "039490")
        kiwoom.set_input_value("기준일자", "20170224")
        kiwoom.set_input_value("수정주가구분", 1)
        kiwoom.comm_rq_data("opt10081_req", "opt10081", 2, "0101")

    df pd.DataFrame(kiwoom.ohlcv, column=['open','high', 'low', 'close', 'volume'], index=kiwoom.ohlcv['date'])

    con = sqlite3.connect("./stock.db")
    df.to_sql(;039490', con, if_exists='replace')
"""
"""
# 싱글데이터로 계좌의 종목현황 데이터
if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

    account_number = kiwoom.get_login_info("ACCNO")
    account_number = account_number.split(';')[0]

    kiwoom.set_input_value("계좌번호", account_number)
    kiwoom.comm_rq_data("opw00018_req", "opw00018", 0, "2000")
"""
"""
# 멀티 데이터를 통해 보유 종목별 평가 잔고 데이터
if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.comm_connect()

rows = self._get_repeat_cnt(trcode, rqname)
for i in range(rows):
    name = self._comm_get_data(trcode, "", rqname, i, "종목명")
    quantity = self._comm_get_data(trcode, "", rqname, i, "보유수량")
    purchase_price = self._comm_get_data(trcode, "", rqname, i, "매입가")
    current_price = self._comm_get_data(trcode, "", rqname, i, "현재가")
    eval_profit_loss_price = self._comm_get_data(trcode, "", rqname, i, "평가손익")
    earning_rate = self._comm_get_data(trcode, "", rqname, i, "수익률(%)")

    quantity = Kiwoom.change_format(quantity)
    purchase_price = Kiwoom.change_format(purchase_price)
    current_price = Kiwoom.change_format(current_price)
    eval_profit_loss_price = Kiwoom.change_format(eval_profit_loss_price)
    earning_rate = Kiwoom.change_format2(earning_rate)

    print(name, quantity, purchase_price, current_price, eval_profit_loss_price, earning_rate)
"""