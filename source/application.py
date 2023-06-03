import sys
from PyQt5.QtWidgets import  QGridLayout,QMainWindow,QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtWidgets import (QApplication)
from PyQt5.QtCore import Qt
from model.wrapper.Wrapper import Wrapper
from view.MainView import MainView
from view.ComparasionView import ComparasionView
import configparser

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        conf = configparser.RawConfigParser()
        conf.read("configuration/config.ini")
        
        self.title = 'Обучающее приложение сегментации объектов дорожного видео'
        self.setWindowTitle(self.title)
        self.setGeometry(conf.getint("dimensions", "left"), 
                         conf.getint("dimensions", "top"), 
                         conf.getint("dimensions", "width"), 
                         conf.getint("dimensions", "heigth"))
        self.setStyleSheet(conf.get("colors", "background"))
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()

class MyTableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        conf = configparser.RawConfigParser()
        conf.read("configuration/config.ini")
        self.setStyleSheet(conf.get("settingsMainWindow", "settings"))
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()

        self.mainTab = QWidget()
        self.comparasionTab = QWidget()

        self.tabs.addTab(self.mainTab,"Главная")
        self.tabs.addTab(self.comparasionTab,"Сравнение результатов")
        self.tabs.setMinimumSize(1500,850)
        self.tabs.setDocumentMode(False)

        model = Wrapper(conf) 
        self.cView = ComparasionView(model,conf)
        self.mView = MainView(self.cView, model,conf)

        self.mainTab.layout = QGridLayout(self)
        self.mainTab.setLayout(self.mainTab.layout)

        self.mainTab.layout.addWidget(self.mView.textBoxSelectionHeader,0,3,0,3)

        self.mainTab.layout.addWidget(self.mView.widgetUploadVideo,1,0,1,3,Qt.AlignmentFlag.AlignTop)
        self.mainTab.layout.addWidget(self.mView.widgetLabel,2,0,1,3,Qt.AlignmentFlag.AlignTop)
        self.mainTab.layout.addWidget(self.mView.widgetRadioButton,1,3,2,3,Qt.AlignmentFlag.AlignTop)

        self.mainTab.layout.addWidget(self.mView.leftMediaplayerWidget,3,0,6,3)
        self.mainTab.layout.addWidget(self.mView.rightMediaplayerWidget,3,3,6,3)

        self.mainTab.layout.addWidget(self.mView.textBoxForResults,9,1,1,4,Qt.AlignmentFlag.AlignTop)
        self.mainTab.layout.addWidget(self.mView.textBoxForRunningSystems,11,0,1,6, Qt.AlignmentFlag.AlignBottom)

        self.comparasionTab.layout = QGridLayout(self)
        self.comparasionTab.setLayout(self.comparasionTab.layout)
        self.comparasionTab.layout.addWidget(self.cView.leftComboBox,0,1,1,1)
        self.comparasionTab.layout.addWidget(self.cView.rightComboBox,0,4,1,1)
        self.comparasionTab.layout.addWidget(self.cView.startButton,1,2,1,2)
        self.comparasionTab.layout.addWidget(self.cView.leftMediaplayerWidget,2,0,3,3)
        self.comparasionTab.layout.addWidget(self.cView.rightMediaplayerWidget,2,3,3,3)
        self.comparasionTab.layout.addWidget(self.cView.textBoxForLeftResults,5,0,2,3,Qt.AlignmentFlag.AlignCenter)
        self.comparasionTab.layout.addWidget(self.cView.textBoxForRightResults,5,3,2,3,Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


