import sys
from PyQt5.QtWidgets import  QGridLayout,QMainWindow,QTabWidget, QVBoxLayout, QWidget
from PyQt5.QtWidgets import (QApplication)
from PyQt5.QtCore import Qt
from source.model.wrapper.Wrapper import Wrapper
from source.view.MainView import MainView
from source.view.ComparasionView import ComparasionView
import warnings

class App(QMainWindow):
    LEFT = 200
    TOP = 100
    WIDTH = 1500
    HEIGTH = 850
    BACKGROUND_COLOR = '#D6D6D6'
    def __init__(self):
        super().__init__()
        self.title = 'Обучающее приложение сегментации объектов дорожного видео'
        self.setWindowTitle(self.title)
        self.setGeometry(self.LEFT, self.TOP, self.WIDTH, self.HEIGTH)
        self.setStyleSheet('background-color:'+ self.BACKGROUND_COLOR)
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        self.show()

class MyTableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.setStyleSheet('font-size: 15pt; font-family: Arial; background: #D6D6D6;')#ВЫНЕСТИ КОНСТАНТЫ!!!!!!
        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()

        self.mainTab = QWidget()
        self.comparasionTab = QWidget()

        self.tabs.addTab(self.mainTab,"Главная")
        self.tabs.addTab(self.comparasionTab,"Сравнение результатов")
        self.tabs.setMinimumSize(1500,850)
        self.tabs.setDocumentMode(False)

        model = Wrapper() 
        self.cView = ComparasionView(model)
        self.mView = MainView(self.cView, model)

        self.mainTab.layout = QGridLayout(self)
        self.mainTab.setLayout(self.mainTab.layout)

        self.mainTab.layout.addWidget(self.mView.textBoxSelectionHeader,0,3,0,3)

        self.mainTab.layout.addWidget(self.mView.widgetUploadVideo,1,0,1,3,Qt.AlignmentFlag.AlignTop)
        self.mainTab.layout.addWidget(self.mView.widgetLabel,2,0,1,3,Qt.AlignmentFlag.AlignTop)
        self.mainTab.layout.addWidget(self.mView.widgetRadioButton,1,3,2,3,Qt.AlignmentFlag.AlignTop)

        #self.mainTab.layout.addWidget(self.mView.startButton,4,3,1,3,Qt.AlignmentFlag.AlignTop)AlignBottom

        self.mainTab.layout.addWidget(self.mView.leftMediaplayerWidget,3,0,6,3)
        self.mainTab.layout.addWidget(self.mView.rightMediaplayerWidget,3,3,6,3)

        self.mainTab.layout.addWidget(self.mView.textBoxForResults,9,1,1,4,Qt.AlignmentFlag.AlignTop)
        self.mainTab.layout.addWidget(self.mView.textBoxForRunningSystems,11,0,1,6, Qt.AlignmentFlag.AlignBottom)

        #model = Wrapper() 
        #self.cView = ComparasionView(model)AlignTop

        self.comparasionTab.layout = QGridLayout(self)
        self.comparasionTab.setLayout(self.comparasionTab.layout)
        self.comparasionTab.layout.addWidget(self.cView.leftComboBox,0,1,1,1)#,Qt.AlignmentFlag.AlignCenter)
        self.comparasionTab.layout.addWidget(self.cView.rightComboBox,0,4,1,1)#,Qt.AlignmentFlag.AlignCenter)
        self.comparasionTab.layout.addWidget(self.cView.startButton,1,2,1,2)#,Qt.AlignmentFlag.AlignCenter)
        self.comparasionTab.layout.addWidget(self.cView.leftMediaplayerWidget,2,0,3,3)#,Qt.AlignmentFlag.AlignHCenter)
        self.comparasionTab.layout.addWidget(self.cView.rightMediaplayerWidget,2,3,3,3)#,Qt.AlignmentFlag.AlignHCenter)
        self.comparasionTab.layout.addWidget(self.cView.textBoxForLeftResults,5,0,2,3,Qt.AlignmentFlag.AlignCenter)
        self.comparasionTab.layout.addWidget(self.cView.textBoxForRightResults,5,3,2,3,Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        
        
if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


