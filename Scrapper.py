import sys

from PyQt5.QtWidgets import *
from Kiwoom import Kiwoom

class Scrapper:
    def __init__(self):
        self.kiwoom = Kiwoom()
        self.kiwoom.comm_connect()

    def run(self):
        print("run")












if __name__ == "__main__":
    app = QApplication(sys.argv)
    scrapper = Scrapper()
    scrapper.run()