

from PyQt5.QtCore import QObject, QSize,Qt
from PyQt5.QtGui import QFont, QColor, QPixmap
from PyQt5.QtWidgets import QApplication, QPushButton, QComboBox, QLineEdit, QListWidget, QListWidgetItem, QCheckBox
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget
import sys

from Mqtt_client import*
from ResurseSO import *

#clasa ce contine informatii despre users
class User:
    def __init__(self, username:str):
        self.username = username
        self.cpuUsageTopic = False
        self.cpuFreqTopic = False

#interfata propriu zisa

class UI:
    def __init__(self):
        self.app = QApplication(sys.argv)

        #main window
        self.window = QWidget()
        self.window.setWindowTitle('MQTT Client')
        self.window.resize(600, 500)
        self.window.move(100, 15)

        self.window.show()

        self.BGimage = QLabel(parent=self.window)

        self.login = QWidget(parent =self.window)






        sys.exit(self.app.exec())


#UI()

