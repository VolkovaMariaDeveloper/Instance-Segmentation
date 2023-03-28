from abc import ABC, abstractmethod
from PyQt5.QtCore import  QUrl
from PyQt5.QtWidgets import QHBoxLayout,QComboBox, QPushButton,QRadioButton,QButtonGroup, QLabel, QVBoxLayout, QWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtGui, QtCore
from mPresenter import MainPresenter
from cPresenter import ComparasionPresenter

class IView(ABC):
    def runVideo(self, path, mediaplayer):
        if path != '':
            mediaplayer.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
            mediaplayer.play()

    def displayText( self,text, textBox):
        textBox.setText(text)

    #@abstractmethod
    def runIndicator(self, persent, mediaplayer):
        pass

    @abstractmethod
    def openTab(self, tab):
        pass
    @abstractmethod
    def runDefaultState():
        pass

class MainView (IView):
    def __init__(self):
        self.empty = QWidget()
        self.uploadVideoButton = QPushButton("Upload")
        self.uploadVideoButton.clicked.connect(self.uploadVideoButtonCliked)
        #self.uploadVideoButton.setGeometry(200, 150, 300, 40)
        self.uploadVideoButton.setFixedSize(150, 30)
        self.uploadVideoButton.setFont(QtGui.QFont('Times', 15))
        self.uploadVideoButton.setStyleSheet('background: white; border-radius: 10px')

        self.uploadLabelButton = QPushButton("")
        
        self.uploadLabelButton.clicked.connect(self.uploadLabelButtonCliked)
        self.uploadLabelButton.setIcon(QtGui.QIcon('uploadLabel.png'))
        self.uploadLabelButton.setFixedSize(40, 30)
        self.uploadLabelButton.setStyleSheet('background: white; border-radius: 5px')

        self.startButton = QPushButton("Start")
        self.startButton.clicked.connect(self.startButtonClicked)
        self.startButton.setFixedSize(150, 30)
        self.startButton.setFont(QtGui.QFont('Times', 15))
        self.startButton.setStyleSheet('background: white; border-radius: 10px')
        
        self.textBoxLeftVideoName = QLabel("LeftVideo")
        self.textBoxLeftVideoName.setFont(QtGui.QFont('Times', 15))
        self.textBoxLeftVideoName.setAlignment(QtCore.Qt.AlignHCenter)
        self.textBoxLeftVideoName.setStyleSheet('background: white; border-radius: 3px')
        self.textBoxLeftVideoName.setFixedSize(700, 30)
        

        self.textBoxRightVideoName = QLabel("RightVideo")
        self.textBoxRightVideoName.setFont(QtGui.QFont('Times', 15))
        self.textBoxRightVideoName.setAlignment(QtCore.Qt.AlignHCenter)
        self.textBoxRightVideoName.setStyleSheet('background: white; border-radius: 3px')
        self.textBoxRightVideoName.setFixedSize(700, 30)

        self.textBoxLabelName =  QLabel('No Label...')
        self.textBoxLabelName.setStyleSheet('background: #bababa; border-radius: 3px')
        self.textBoxLabelName.setFixedSize(200, 30)
        self.textBoxLabelName.setFont(QtGui.QFont('Times', 15))
        self.textBoxLabelName.setAlignment(QtCore.Qt.AlignCenter)

        self.widgetLabel = QWidget()
        self.layoutLabel = QHBoxLayout()
        self.layoutLabel.addWidget(self.textBoxLabelName,QtCore.Qt.AlignRight)
        self.layoutLabel.addWidget(self.uploadLabelButton,QtCore.Qt.AlignRight)
        self.widgetLabel.setLayout(self.layoutLabel)

        self.textBoxForResults = QLabel("Results")
        self.textBoxForResults.setAlignment(QtCore.Qt.AlignHCenter)
        self.textBoxForResults.setFont(QtGui.QFont('Times', 15))
        
        self.firstRadioButton = QRadioButton('BlendMask')
        self.firstRadioButton.setFont(QtGui.QFont('Times', 15))
        self.firstRadioButton.setFixedSize(200, 30)
        self.firstRadioButton.setStyleSheet("QRadioButton" "{""spacing : 100px;""}")
        self.firstRadioButton.setStyleSheet('background: #bababa; border-radius: 3px')
        self.firstRadioButton.setChecked(True)

        self.secondRadioButton = QRadioButton('PolarMask')
        self.secondRadioButton.setFont(QtGui.QFont('Times', 15))
        self.secondRadioButton.setFixedSize(200, 30)
        self.secondRadioButton.setStyleSheet("QRadioButton" "{""spacing : 100px;""}")
        self.secondRadioButton.setStyleSheet('background: #bababa; border-radius: 3px')

        self.thirdRadioButton = QRadioButton('YOLACT')
        self.thirdRadioButton.setFont(QtGui.QFont('Times', 15))
        self.thirdRadioButton.setFixedSize(200, 30)
        self.thirdRadioButton.setStyleSheet("QRadioButton" "{""spacing : 100px;""}")
        self.thirdRadioButton.setStyleSheet('background: #bababa; border-radius: 3px')

        self.widgetRadioButton = QWidget()
        self.layoutRadioButton = QHBoxLayout()
        self.layoutRadioButton.addWidget(self.firstRadioButton)
        self.layoutRadioButton.addWidget(self.secondRadioButton)
        self.layoutRadioButton.addWidget(self.thirdRadioButton)
        self.widgetRadioButton.setLayout(self.layoutRadioButton)

        self.buttonGroup = QButtonGroup()
        self.buttonGroup.addButton(self.firstRadioButton)
        self.buttonGroup.addButton(self.secondRadioButton)
        self.buttonGroup.addButton(self.thirdRadioButton)
        self.buttonGroup.buttonClicked.connect(self._on_radio_button_clicked)

        self.leftMediaplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.leftVideoWidget = QVideoWidget()
        self.leftMediaplayerWidget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.leftVideoWidget)
        layout.addWidget(self.textBoxLeftVideoName, QtCore.Qt.AlignBottom)
        layout.setContentsMargins(0, 0, 0, 0)#Где еще можно использвать?
        self.leftMediaplayerWidget.setStyleSheet('background: #bababa; border-radius: 3px')
        self.leftMediaplayerWidget.setLayout(layout)
        self.leftMediaplayer.setVideoOutput(self.leftVideoWidget)

        self.rightMediaplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.rightVideoWidget = QVideoWidget()
        self.rightMediaplayerWidget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.rightVideoWidget)
        layout.addWidget(self.textBoxRightVideoName, QtCore.Qt.AlignBottom)
        layout.setContentsMargins(0, 0, 0, 0)
        self.rightMediaplayerWidget.setStyleSheet('background: #bababa; border-radius: 3px')
        self.rightMediaplayerWidget.setLayout(layout)
        self.rightMediaplayer.setVideoOutput(self.rightVideoWidget)
       
        self.textBoxForRunningSystems = QLabel("Running Systems")
        self.textBoxForRunningSystems.setFont(QtGui.QFont('Times', 15))
        self.textBoxForRunningSystems.setAlignment(QtCore.Qt.AlignHCenter)

        self.nameOfSystemSegmentation = 'BlendMask'
        self.mPresenter =  MainPresenter(self)

    def uploadVideoButtonCliked(self):
        #self.runDefaultState()
        self.mPresenter.onUploadVideoButtonClick()
        
    def uploadLabelButtonCliked(self):
        self.mPresenter.onUploadLabelButtonClick()
            
    def _on_radio_button_clicked(self, button):
        button.setChecked(True)
        self.nameOfSystemSegmentation = button.text()

    def startButtonClicked(self):
        #self.runIndicator()    
        self.mPresenter.onStartButtonClick(self.nameOfSystemSegmentation)

    def openTab():
        pass
    
    def runDefaultState():
        pass


class ComparasionView(IView):
    def __init__(self, model):
        self.leftComboBox = QComboBox()
        self.leftComboBox.setFixedSize(350, 30)
        self.rightComboBox = QComboBox()
        self.rightComboBox.setFixedSize(350, 30)
        self.leftComboBox.activated[str].connect(
            self.onSelectedLeftComboBox)
        self.leftComboBox.activated[str].connect(self.onSelectedRightComboBox)

        self.startButton = QPushButton("Start")
        self.startButton.clicked.connect(self.startButtonClicked)
        self.startButton.setFixedSize(150, 30)
        self.startButton.setFont(QtGui.QFont('Times', 15))
        self.startButton.setStyleSheet('background: white; border-radius: 10px')

        self.textBoxLeftVideoName = QLabel("Left video")
        self.textBoxLeftVideoName.setFont(QtGui.QFont('Times', 15))
        self.textBoxLeftVideoName.setAlignment(QtCore.Qt.AlignHCenter)
        self.textBoxLeftVideoName.setStyleSheet('background: white; border-radius: 3px')
        self.textBoxLeftVideoName.setFixedSize(700, 30)

        self.textBoxRightVideoName = QLabel("Right video")
        self.textBoxRightVideoName.setFont(QtGui.QFont('Times', 15))
        self.textBoxRightVideoName.setAlignment(QtCore.Qt.AlignHCenter)
        self.textBoxRightVideoName.setStyleSheet('background: white; border-radius: 3px')
        self.textBoxRightVideoName.setFixedSize(700, 30)

        self.textBoxForLeftResults = QLabel("Left results")
        self.textBoxForLeftResults.setAlignment(QtCore.Qt.AlignHCenter)
        self.textBoxForLeftResults.setFont(QtGui.QFont('Times', 15))

        self.textBoxForRightResults = QLabel("Right results")
        self.textBoxForRightResults.setAlignment(QtCore.Qt.AlignHCenter)
        self.textBoxForRightResults.setFont(QtGui.QFont('Times', 15))

        self.leftMediaplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
       
        self.leftVideoWidget = QVideoWidget()
        self.leftMediaplayerWidget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.leftVideoWidget)
        layout.addWidget(self.textBoxLeftVideoName, QtCore.Qt.AlignBottom)
        layout.setContentsMargins(0, 0, 0, 0)#Где еще можно использвать?
        self.leftMediaplayerWidget.setStyleSheet('background: #bababa; border-radius: 3px')
        self.leftMediaplayerWidget.setLayout(layout)
        self.leftMediaplayer.setVideoOutput(self.leftVideoWidget)

        self.rightMediaplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.rightVideoWidget = QVideoWidget()
        self.rightMediaplayerWidget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.rightVideoWidget)
        layout.addWidget(self.textBoxRightVideoName, QtCore.Qt.AlignBottom)
        layout.setContentsMargins(0, 0, 0, 0)
        self.rightMediaplayerWidget.setStyleSheet('background: #bababa; border-radius: 3px')
        self.rightMediaplayerWidget.setLayout(layout)
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

    def openTab():
        pass