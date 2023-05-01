from abc import ABC, abstractmethod
from PyQt5.QtCore import  QUrl
from PyQt5.QtWidgets import QGridLayout,QComboBox, QPushButton,QRadioButton,QButtonGroup, QLabel, QVBoxLayout, QWidget
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
    BUTTON_COLOR =  "white"
    FRAME_COLOR = "#bababa"
    PATH_TO_IMAGE_FOLDER ="images/folderImg.png"
    def __init__(self):
        self.empty = QWidget()
        self.uploadLabelButton = QPushButton("")
       
        self.uploadLabelButton.clicked.connect(self.uploadLabelButtonCliked)
        self.uploadLabelButton.setIcon(QtGui.QIcon(self.PATH_TO_IMAGE_FOLDER))
        self.uploadLabelButton.setStyleSheet('background:' + self.BUTTON_COLOR)

        self.uploadVideoButton = QPushButton("")
        self.uploadVideoButton.clicked.connect(self.uploadVideoButtonCliked)
        self.uploadVideoButton.setIcon(QtGui.QIcon(self.PATH_TO_IMAGE_FOLDER))
        self.uploadVideoButton.setStyleSheet('background:'+ self.BUTTON_COLOR)

        self.startButton = QPushButton("Start")
        self.startButton.clicked.connect(self.startButtonClicked)
        self.startButton.setStyleSheet('background:'+ self.BUTTON_COLOR)
        
        self.textBoxLeftVideoName = QLabel("LeftVideo")
        self.textBoxRightVideoName = QLabel("RightVideo")
       
        self.textBoxLabelName =  QLabel('No Lable...')
        self.textBoxLabelName.setAlignment(QtCore.Qt.AlignCenter)
       
        self.textBoxVideoPath =  QLabel('Select video...')
        self.textBoxVideoPath.setAlignment(QtCore.Qt.AlignCenter)

        self.layoutUploadVideo = QGridLayout()
        self.layoutUploadVideo.addWidget(self.textBoxVideoPath,0,0,1,4)
        self.layoutUploadVideo.addWidget(self.uploadVideoButton,0,4,1,1)
        self.widgetUploadVideo = QWidget()
        self.widgetUploadVideo.setLayout(self.layoutUploadVideo)

        self.layoutLabel = QGridLayout()
        self.layoutLabel.addWidget(self.textBoxLabelName,0,0,1,4)
        self.layoutLabel.addWidget(self.uploadLabelButton,0,4,1,1)
        self.widgetLabel = QWidget()
        self.widgetLabel.setLayout(self.layoutLabel)

        self.textBoxForResults = QLabel("Results")
        self.textBoxForResults.setAlignment(QtCore.Qt.AlignHCenter)

        self.textBoxSelectionHeader = QLabel("Select segmented system")
        self.textBoxSelectionHeader.setAlignment(QtCore.Qt.AlignHCenter)
        
        self.firstRadioButton = QRadioButton('BlendMask')
        self.firstRadioButton.setChecked(True)
        self.secondRadioButton = QRadioButton('PolarMask')
        self.thirdRadioButton = QRadioButton('YOLACT')

        self.layoutRadioButton = QGridLayout()
        self.layoutRadioButton.addWidget(self.textBoxSelectionHeader,0,0,1,1, Qt.AlignmentFlag.AlignCenter)
        self.layoutRadioButton.addWidget(self.firstRadioButton,1,0,1,1, Qt.AlignmentFlag.AlignLeft)
        self.layoutRadioButton.addWidget(self.secondRadioButton,2,0,1,1, Qt.AlignmentFlag.AlignLeft)
        self.layoutRadioButton.addWidget(self.thirdRadioButton,3,0,1,1, Qt.AlignmentFlag.AlignLeft)
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
        self.leftVideoWidget.setStyleSheet('background:'+ self.FRAME_COLOR)
        self.leftMediaplayerWidget = QWidget() 

        self.layout = QGridLayout()
        self.layout.addWidget(self.leftVideoWidget,0,0,6,6)
        self.layout.addWidget(self.textBoxLeftVideoName,6,0,1,6,Qt.AlignmentFlag.AlignCenter)
        self.leftMediaplayerWidget.setLayout(self.layout)
        self.leftMediaplayer.setVideoOutput(self.leftVideoWidget)

        self.rightMediaplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.rightVideoWidget = QVideoWidget()
        self.rightVideoWidget.setStyleSheet('background:'+ self.FRAME_COLOR)
        self.rightMediaplayerWidget = QWidget()

        self.layout = QGridLayout()
        self.layout.addWidget(self.rightVideoWidget,0,0,6,6)
        self.layout.addWidget(self.textBoxRightVideoName,6,0,1,6,Qt.AlignmentFlag.AlignCenter)
        self.rightMediaplayerWidget.setLayout(self.layout)
        self.rightMediaplayer.setVideoOutput(self.rightVideoWidget)
       
        self.textBoxForRunningSystems = QLabel("Running Systems")
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
    BUTTON_COLOR =  "white"
    FRAME_COLOR ="#bababa"
    def __init__(self, model):
        self.leftComboBox = QComboBox()
        self.rightComboBox = QComboBox()
        self.leftComboBox.activated[str].connect(
            self.onSelectedLeftComboBox)
        self.leftComboBox.activated[str].connect(self.onSelectedRightComboBox)

        self.startButton = QPushButton("Start")
        self.startButton.clicked.connect(self.startButtonClicked)
        self.startButton.setStyleSheet('background:' + self.BUTTON_COLOR)

        self.textBoxLeftVideoName = QLabel("Left video")
        self.textBoxLeftVideoName.setAlignment(QtCore.Qt.AlignHCenter)

        self.textBoxRightVideoName = QLabel("Right video")
        self.textBoxRightVideoName.setAlignment(QtCore.Qt.AlignHCenter)

        self.textBoxForLeftResults = QLabel("Left results")
        self.textBoxForLeftResults.setAlignment(QtCore.Qt.AlignHCenter)

        self.textBoxForRightResults = QLabel("Right results")
        self.textBoxForRightResults.setAlignment(QtCore.Qt.AlignHCenter)

        self.leftMediaplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.leftVideoWidget = QVideoWidget()
        self.leftVideoWidget.setStyleSheet('background:'+ self.FRAME_COLOR)
        self.leftMediaplayerWidget = QWidget() 

        self.layout = QGridLayout()
        self.layout.addWidget(self.leftVideoWidget,0,0,6,6)
        self.layout.addWidget(self.textBoxLeftVideoName,6,0,1,6,Qt.AlignmentFlag.AlignCenter)
        self.leftMediaplayerWidget.setLayout(self.layout)
        self.leftMediaplayer.setVideoOutput(self.leftVideoWidget)

        self.rightMediaplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.rightVideoWidget = QVideoWidget()
        self.rightVideoWidget.setStyleSheet('background:'+ self.FRAME_COLOR)
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

    def openTab():
        pass