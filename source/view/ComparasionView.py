from PyQt5.QtWidgets import QGridLayout,QComboBox, QPushButton,QLabel, QWidget, QErrorMessage
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import  QtCore
from presenter.cPresenter import ComparasionPresenter
from PyQt5.QtCore import Qt
from view.IView import IView

class ComparasionView(IView):
    def __init__(self, model, conf):
        self.conf = conf
        self.conf.read("configuration/config.ini")
        self.nonStartedSystemError = QErrorMessage()
        self.leftComboBox = QComboBox()
        self.rightComboBox = QComboBox()
        self.leftComboBox.activated[str].connect(self.onSelectedLeftComboBox)
        self.leftComboBox.activated[str].connect(self.onSelectedRightComboBox)

        self.startButton = QPushButton("Старт")
        self.startButton.clicked.connect(self.startButtonClicked)
        self.startButton.setStyleSheet(self.conf.get("colors", "button"))

        self.textBoxLeftVideoName = QLabel("")
        self.textBoxLeftVideoName.setAlignment(QtCore.Qt.AlignHCenter)

        self.textBoxRightVideoName = QLabel("")
        self.textBoxRightVideoName.setAlignment(QtCore.Qt.AlignHCenter)

        self.textBoxForLeftResults = QLabel("")
        self.textBoxForLeftResults.setAlignment(QtCore.Qt.AlignHCenter)

        self.textBoxForRightResults = QLabel("")
        self.textBoxForRightResults.setAlignment(QtCore.Qt.AlignHCenter)

        self.leftMediaplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.leftVideoWidget = QVideoWidget()        
        self.leftVideoWidget.setMaximumWidth(880)
        self.leftVideoWidget.setMaximumHeight(320)

        self.leftVideoWidget.setStyleSheet(self.conf.get("colors", "frame"))
        self.leftMediaplayerWidget = QWidget() 

        self.layout = QGridLayout()
        self.layout.addWidget(self.leftVideoWidget,0,0,6,6)
        self.layout.addWidget(self.textBoxLeftVideoName,6,0,1,6,Qt.AlignmentFlag.AlignCenter)
        self.leftMediaplayerWidget.setLayout(self.layout)
        self.leftMediaplayer.setVideoOutput(self.leftVideoWidget)

        self.rightMediaplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.rightVideoWidget = QVideoWidget()
        self.rightVideoWidget.setMaximumWidth(880)
        self.rightVideoWidget.setMaximumHeight(320)
        self.rightVideoWidget.setStyleSheet(self.conf.get("colors", "frame"))
        self.rightMediaplayerWidget = QWidget()

        self.layout = QGridLayout()
        self.layout.addWidget(self.rightVideoWidget,0,0,6,6)
        self.layout.addWidget(self.textBoxRightVideoName,6,0,1,6,Qt.AlignmentFlag.AlignCenter)
        self.rightMediaplayerWidget.setLayout(self.layout)
        self.rightMediaplayer.setVideoOutput(self.rightVideoWidget)

        self.cPresenter =  ComparasionPresenter(self,model)

    def runDefaultState(self):
        self.leftComboBox.clear()
        self.rightComboBox.clear()

    def addSystemForComparation(self, nameSystem):
        self.leftComboBox.addItem(nameSystem)
        self.rightComboBox.addItem(nameSystem)
    
    def onSelectedLeftComboBox(self):
        self.leftSystemName = self.leftComboBox.currentText()

    def onSelectedRightComboBox(self):
        self.rightSystemName = self.rightComboBox.currentText()

    def startButtonClicked(self):
        self.cPresenter.onStartButtonClick()
