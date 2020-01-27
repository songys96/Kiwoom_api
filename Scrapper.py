import sys
import time
from pandas import DataFrame

from PyQt5.QtWidgets import *
from Kiwoom import Kiwoom

MARKET_KOSPI = 0
MARKET_KOSDAQ = 10

class Scrapper:
    def __init__(self):
        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()
        self.get_code_list()

    def run(self):
        df = self.get_ohlcv("039490", "20170321")
        print(df)

    def get_code_list(self):
        self.kospi_codes = self.kiwoom.get_code_list_by_market(MARKET_KOSPI)
        self.kosdaq_codes = self.kiwoom.get_code_list_by_market(MARKET_KOSDAQ)

    def get_ohlcv(self, code, start):
        self.kiwoom.ohlcv = {'date': [], 'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}

        self.kiwoom.set_input_value("종목코드", code)
        self.kiwoom.set_input_value("기준일자", start)
        self.kiwoom.set_input_value("수정주가구분", 1)
        self.kiwoom.comm_rq_data("opt10081_req", "opt10081", 0, "0101")
        time.sleep(0.2)

        df = DataFrame(self.kiwoom.ohlcv, columns = ['open', "high", "low", "close", "volume"], index=self.kiwoom.ohlcv['date'])
        return df











if __name__ == "__main__":
    app = QApplication(sys.argv)
    scrapper = Scrapper()
    scrapper.run()