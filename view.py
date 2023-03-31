from abc import ABC, abstractmethod
from PyQt5.QtCore import  QUrl
from PyQt5.QtWidgets import QGridLayout,QSizePolicy,QComboBox, QPushButton,QRadioButton,QButtonGroup, QLabel, QVBoxLayout, QWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtGui, QtCore
from mPresenter import MainPresenter
from cPresenter import ComparasionPresenter
from PyQt5.QtCore import Qt

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

        self.uploadLabelButton = QPushButton("")
       
        self.uploadLabelButton.clicked.connect(self.uploadLabelButtonCliked)
        self.uploadLabelButton.setIcon(QtGui.QIcon('uploadLabel.png'))
        #self.uploadLabelButton.resize(40, 30)
        self.uploadLabelButton.setStyleSheet('background: white')

        self.uploadVideoButton = QPushButton("")
        self.uploadVideoButton.clicked.connect(self.uploadVideoButtonCliked)
        self.uploadVideoButton.setIcon(QtGui.QIcon('uploadLabel.png'))
        #self.uploadVideoButton.resize(40, 30)
        self.uploadVideoButton.setStyleSheet('background: white')

        self.startButton = QPushButton("Start")
        self.startButton.clicked.connect(self.startButtonClicked)
       # self.startButton.resize(150, 30)
        self.startButton.setFont(QtGui.QFont('Times', 15))
        self.startButton.setStyleSheet('background: white')
        
        self.textBoxLeftVideoName = QLabel("LeftVideo")
        self.textBoxLeftVideoName.setFont(QtGui.QFont('Times', 15))
        self.textBoxLeftVideoName.setAlignment(QtCore.Qt.AlignHCenter)
        #self.textBoxLeftVideoName.setStyleSheet('background: white')
        #self.textBoxLeftVideoName.minimumSize(700)
        
        self.textBoxRightVideoName = QLabel("RightVideo")
        self.textBoxRightVideoName.setFont(QtGui.QFont('Times', 15))
        self.textBoxRightVideoName.setAlignment(QtCore.Qt.AlignHCenter)
       # self.textBoxRightVideoName.setStyleSheet('background: white')
       # self.textBoxRightVideoName.setFixedSize(700, 30)

        self.textBoxLabelName =  QLabel('No Lable...')
        self.textBoxLabelName.setStyleSheet('background: #bababa')
        self.textBoxLabelName.resize(200, 20)
        self.textBoxLabelName.setFont(QtGui.QFont('Times', 15))
        self.textBoxLabelName.setAlignment(QtCore.Qt.AlignCenter)
       

        self.textBoxVideoPath =  QLabel('Select video...')
        self.textBoxVideoPath.setStyleSheet('background: #bababa')
        self.textBoxVideoPath.resize(200, 20)
        self.textBoxVideoPath.setFont(QtGui.QFont('Times', 15))
        self.textBoxVideoPath.setAlignment(QtCore.Qt.AlignCenter)
       # self.textBoxVideoPath.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        self.layoutUploadVideo = QGridLayout()
        self.layoutUploadVideo.addWidget(self.textBoxVideoPath,0,0,1,4)#, Qt.AlignmentFlag.AlignRight)
        self.layoutUploadVideo.addWidget(self.uploadVideoButton,0,4,1,1)
        self.widgetUploadVideo = QWidget()
        self.widgetUploadVideo.setLayout(self.layoutUploadVideo)
        #self.widgetUploadVideo.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        self.layoutLabel = QGridLayout()
        self.layoutLabel.addWidget(self.textBoxLabelName,0,0,1,4)#, Qt.AlignmentFlag.AlignRight)
        self.layoutLabel.addWidget(self.uploadLabelButton,0,4,1,1)
        self.widgetLabel = QWidget()
        self.widgetLabel.setLayout(self.layoutLabel)

        self.textBoxForResults = QLabel("Results")
        self.textBoxForResults.setAlignment(QtCore.Qt.AlignHCenter)
        self.textBoxForResults.setFont(QtGui.QFont('Times', 15))

        self.textBoxSelectionHeader = QLabel("Select segmented system")
        self.textBoxSelectionHeader.setAlignment(QtCore.Qt.AlignHCenter)
        self.textBoxSelectionHeader.setFont(QtGui.QFont('Times', 15))
        
        self.firstRadioButton = QRadioButton('BlendMask')
        self.firstRadioButton.setFont(QtGui.QFont('Times', 15))
        self.firstRadioButton.setChecked(True)

        self.secondRadioButton = QRadioButton('PolarMask')
        self.secondRadioButton.setFont(QtGui.QFont('Times', 15))

        self.thirdRadioButton = QRadioButton('YOLACT')
        self.thirdRadioButton.setFont(QtGui.QFont('Times', 15))

        self.layoutRadioButton = QGridLayout()
        self.layoutRadioButton.addWidget(self.textBoxSelectionHeader,0,0,1,1, Qt.AlignmentFlag.AlignCenter)
        self.layoutRadioButton.addWidget(self.firstRadioButton,1,0,1,1, Qt.AlignmentFlag.AlignCenter)
        self.layoutRadioButton.addWidget(self.secondRadioButton,2,0,1,1, Qt.AlignmentFlag.AlignCenter)
        self.layoutRadioButton.addWidget(self.thirdRadioButton,3,0,1,1, Qt.AlignmentFlag.AlignCenter)
        self.layoutRadioButton.addWidget(self.startButton,4,0,1,1, Qt.AlignmentFlag.AlignCenter)
        self.widgetRadioButton = QWidget()
        self.widgetRadioButton.setLayout(self.layoutRadioButton)

        self.buttonGroup = QButtonGroup()
        self.buttonGroup.addButton(self.firstRadioButton)
        self.buttonGroup.addButton(self.secondRadioButton)
        self.buttonGroup.addButton(self.thirdRadioButton)
        self.buttonGroup.buttonClicked.connect(self._on_radio_button_clicked)

        self.leftMediaplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.leftVideoWidget = QVideoWidget()
        self.leftMediaplayerWidget = QWidget() 

        self.layout = QGridLayout()
        self.layout.addWidget(self.leftVideoWidget,0,0,6,6)
        self.layout.addWidget(self.textBoxLeftVideoName,6,0,1,6,Qt.AlignmentFlag.AlignCenter)
        self.leftMediaplayerWidget.setStyleSheet('background: #bababa')
        self.leftMediaplayerWidget.setLayout(self.layout)
        self.leftMediaplayer.setVideoOutput(self.leftVideoWidget)

        self.rightMediaplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.rightVideoWidget = QVideoWidget()
        self.rightMediaplayerWidget = QWidget()

        self.layout = QGridLayout()
        self.layout.addWidget(self.rightVideoWidget,0,0,6,6)
        self.layout.addWidget(self.textBoxRightVideoName,6,0,1,6,Qt.AlignmentFlag.AlignCenter)
        self.rightMediaplayerWidget.setStyleSheet('background: #bababa')
        self.rightMediaplayerWidget.setLayout(self.layout)
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
        #self.leftComboBox.setFixedSize(350, 30)
        self.rightComboBox = QComboBox()
       # self.rightComboBox.setFixedSize(350, 30)
        self.leftComboBox.activated[str].connect(
            self.onSelectedLeftComboBox)
        self.leftComboBox.activated[str].connect(self.onSelectedRightComboBox)

        self.startButton = QPushButton("Start")
        self.startButton.clicked.connect(self.startButtonClicked)
        #self.startButton.setFixedSize(150, 30)
        self.startButton.setFont(QtGui.QFont('Times', 15))
        self.startButton.setStyleSheet('background: white')

        self.textBoxLeftVideoName = QLabel("Left video")
        self.textBoxLeftVideoName.setFont(QtGui.QFont('Times', 15))
        self.textBoxLeftVideoName.setAlignment(QtCore.Qt.AlignHCenter)
        self.textBoxLeftVideoName.setStyleSheet('background: white')
       # self.textBoxLeftVideoName.setFixedSize(700, 30)

        self.textBoxRightVideoName = QLabel("Right video")
        self.textBoxRightVideoName.setFont(QtGui.QFont('Times', 15))
        self.textBoxRightVideoName.setAlignment(QtCore.Qt.AlignHCenter)
        self.textBoxRightVideoName.setStyleSheet('background: white')
        #self.textBoxRightVideoName.setFixedSize(700, 30)

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
        self.leftMediaplayerWidget.setStyleSheet('background: #bababa')
        self.leftMediaplayerWidget.setLayout(layout)
        self.leftMediaplayer.setVideoOutput(self.leftVideoWidget)

        self.rightMediaplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.rightVideoWidget = QVideoWidget()
        self.rightMediaplayerWidget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.rightVideoWidget)
        layout.addWidget(self.textBoxRightVideoName, QtCore.Qt.AlignBottom)
        layout.setContentsMargins(0, 0, 0, 0)
        self.rightMediaplayerWidget.setStyleSheet('background: #bababa')
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