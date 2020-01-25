# -*- coding:utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *

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
    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, Qstring)", trcode, rqname)
        return ret

    # 
    def _receive_tr_data(self, screen_no, rqname, record_name, next, unused1, unused2, unused3, unused4):
        if next == "2":
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10081_req":
            self._opt10081(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError():
            pass

    def _opt10081(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)

        for i in range(data_cnt):
            data = self._comm_get_data(trcode, "", rqname, i, "일자")
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




"""
# 여기는 단일 실행시 필요
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
        time.sleep(TR_REQ_TIME_INTERVAL)
        kiwoom.set_input_value("종목코드", "039490")
        kiwoom.set_input_value("기준일자", "20170224")
        kiwoom.set_input_value("수정주가구분", 1)
        kiwoom.comm_rq_data("opt10081_req", "opt10081", 2, "0101")

    df pd.DataFrame(kiwoom.ohlcv, column=['open','high', 'low', 'close', 'volume'], index=kiwoom.ohlcv['date'])

    con = sqlite3.connect("./stock.db")
    df.to_sql(;039490', con, if_exists='replace')
"""