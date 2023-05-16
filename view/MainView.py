from PyQt5.QtWidgets import QGridLayout, QPushButton,QRadioButton,QButtonGroup, QLabel, QWidget
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtGui, QtCore
from presenter.mPresenter import MainPresenter

from PyQt5.QtCore import Qt
from view.IView import IView

class MainView (IView):
    BUTTON_COLOR =  "white"
    FRAME_COLOR = "#bababa"
    PATH_TO_IMAGE_FOLDER ="images/folderImg.png"
    #def __getattr__(self, item):
   #     return IView.__dict__[item]

    def __init__(self, cView, model):
        self.cView = cView
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
        
        self.textBoxLeftVideoName = QLabel("")
        self.textBoxRightVideoName = QLabel("")
       
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

        self.textBoxForResults = QLabel("")
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
       
        self.textBoxForRunningSystems = QLabel("")
        self.textBoxForRunningSystems.setAlignment(QtCore.Qt.AlignHCenter)

        self.nameOfSystemSegmentation = 'BlendMask'
        self.mPresenter =  MainPresenter(self,self.cView, model)

    def uploadVideoButtonCliked(self):
        self.runDefaultState()
        self.mPresenter.onUploadVideoButtonClick()
        
    def uploadLabelButtonCliked(self):
        self.mPresenter.onUploadLabelButtonClick()
            
    def _on_radio_button_clicked(self, button):
        button.setChecked(True)
        self.nameOfSystemSegmentation = button.text()

    def startButtonClicked(self):
        #self.runIndicator()    
        self.mPresenter.onStartButtonClick(self.nameOfSystemSegmentation)
    
    def runDefaultState(self):
        self.textBoxForRunningSystems.setText("")
        self.textBoxLeftVideoName.setText("")
        self.textBoxRightVideoName.setText("")
        self.rightVideoWidget.setStyleSheet('background:'+ self.FRAME_COLOR)
        self.textBoxForResults.setText("")
        self.textBoxLabelName.setText('No Lable...')
        self.mPresenter.runningSystemsSet.clear()
        self.cView.leftComboBox.clear()
        self.cView.rightComboBox.clear()
        self.cView.textBoxLeftVideoName.setText("")
        self.cView.textBoxRightVideoName.setText("")
        self.cView.textBoxForLeftResults.setText("")
        self.cView.textBoxForRightResults.setText("")
        self.cView.leftVideoWidget.setStyleSheet('background:'+ self.FRAME_COLOR)
        self.cView.rightVideoWidget.setStyleSheet('background:'+ self.FRAME_COLOR)
       
