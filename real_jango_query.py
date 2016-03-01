import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("추정자산조회")
        self.setGeometry(300, 300, 300, 150)

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.kiwoom.dynamicCall("CommConnect()")
        self.kiwoom.connect(self.kiwoom, SIGNAL("OnEventConnect(int)"), self.OnEventConnect)
        self.kiwoom.connect(self.kiwoom, SIGNAL("OnReceiveTrData(QString, QString, QString, QString, QString, int, QString, QString, QString)"), self.OnReceiveTrData)

        self.setupUI()

    def setupUI(self):
        btn1 = QPushButton("계좌 얻기", self)
        btn1.move(190, 20)
        btn1.clicked.connect(self.btn1_clicked)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(10, 60, 280, 80)

    def btn1_clicked(self):
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "계좌번호", "3811412211")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "비밀번호", "3255")
        self.kiwoom.dynamicCall("SetInputValue(QString, QString)", "상장폐지조회구분", "0")
        self.kiwoom.dynamicCall("CommRqData(QString, QString, int, QString)", "RQName", "OPW00003", 0, "0101")

    def OnReceiveTrData(self, ScrNo, RQName, TrCode, RecordName, PrevNext, DataLength, ErrorCode, Message, SplmMsg):
        if RQName == "RQName":
            name = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", TrCode, "", RQName, 0, "종목명")
            volume = self.kiwoom.dynamicCall("CommGetData(QString, QString, QString, int, QString)", TrCode, "", RQName, 0, "거래량")

            self.text_edit.append("종목명: " + name.strip())
            self.text_edit.append("거래량: " + volume.strip())
            
    def OnEventConnect(self, ErrCode):
        if ErrCode == 0:
            self.text_edit.append("로그인 성공")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()