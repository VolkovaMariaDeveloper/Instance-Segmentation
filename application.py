from PyQt5.QtWidgets import  QGridLayout,QMainWindow,QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtWidgets import (QApplication)
import sys
from PyQt5.QtCore import Qt
from model import Model
from view import MainView, ComparasionView

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 tabs - pythonspot.com'
        self.left = 200
        self.top = 100
        self.width = 1500
        self.height = 850
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("background-color: #D6D6D6;")
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()

class MyTableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        #self.setStyleSheet('font-size: 18pt; font-family: Courier;')

        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet('font-size: 15pt; font-family: Times;')
        self.mainTab = QWidget()
        self.comparasionTab = QWidget()


        self.tabs.addTab(self.mainTab,"Main")
        self.tabs.addTab(self.comparasionTab,"Comparasion")
        self.tabs.resize(1500,850)
        self.tabs.setDocumentMode(True)

        self.mView = MainView()

        self.mainTab.layout = QGridLayout(self)
        self.mainTab.setLayout(self.mainTab.layout)
      

        self.mainTab.layout.addWidget(self.mView.uploadVideoButton,0,0,1,1, Qt.AlignmentFlag.AlignRight)
        self.mainTab.layout.addWidget(self.mView.widgetLabel,0,1,1,1, Qt.AlignmentFlag.AlignRight)
        self.mainTab.layout.addWidget(self.mView.widgetRadioButton,0,2,1,3)#,Qt.AlignmentFlag.AlignCenter)

        self.mainTab.layout.addWidget(self.mView.startButton,0,5,1,1,Qt.AlignmentFlag.AlignLeft)
        self.mainTab.layout.addWidget(self.mView.leftMediaplayerWidget,2,0,3,3,Qt.AlignmentFlag.AlignHCenter)
        self.mainTab.layout.addWidget(self.mView.rightMediaplayerWidget,2,3,3,3,Qt.AlignmentFlag.AlignHCenter)

        self.mainTab.layout.addWidget(self.mView.textBoxForResults,5,1,1,4,Qt.AlignmentFlag.AlignCenter)
        self.mainTab.layout.addWidget(self.mView.textBoxForRunningSystems,6,0,1,6, Qt.AlignmentFlag.AlignBottom)
        self.mainTab.layout.addWidget(self.mView.empty,1,0,1,6, Qt.AlignmentFlag.AlignBottom)
       
        model = Model() 
        self.cView = ComparasionView(model)

        self.comparasionTab.layout = QGridLayout(self)
        self.comparasionTab.setLayout(self.comparasionTab.layout)
        self.comparasionTab.layout.addWidget(self.cView.leftComboBox,0,1,1,1,Qt.AlignmentFlag.AlignCenter)
        self.comparasionTab.layout.addWidget(self.cView.rightComboBox,0,4,1,1,Qt.AlignmentFlag.AlignCenter)
        self.comparasionTab.layout.addWidget(self.cView.startButton,1,0,1,6,Qt.AlignmentFlag.AlignCenter)
        self.comparasionTab.layout.addWidget(self.cView.leftMediaplayerWidget,2,0,3,3,Qt.AlignmentFlag.AlignHCenter)
        self.comparasionTab.layout.addWidget(self.cView.rightMediaplayerWidget,2,3,3,3,Qt.AlignmentFlag.AlignHCenter)
        self.comparasionTab.layout.addWidget(self.cView.textBoxForLeftResults,5,0,2,3,Qt.AlignmentFlag.AlignCenter)
        self.comparasionTab.layout.addWidget(self.cView.textBoxForRightResults,5,3,2,3,Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


