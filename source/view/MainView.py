from PyQt5.QtWidgets import QGridLayout, QPushButton,QRadioButton,QButtonGroup, QLabel, QWidget, QProgressBar, QMessageBox
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtGui, QtCore
from presenter.mPresenter import MainPresenter
from PyQt5.QtCore import Qt
from view.IView import IView


class MainView (IView):
    BUTTON_COLOR = "white"
    FRAME_COLOR = "#bababa"
    START = "Старт"
    WARNING_RESTART = "Данное действие выполнить невозможно, дождитесь окончания сегментации предыдущей системы"
    WARNING_NOT_VIDEO = "Перед запуском сегментации загрузите видео"
    WARNING = "Пердупреждение"
    CHANGE_VIDEO = "Выберите видео..."
    CHANGE_SYSTEM = "Выберите систему сегментации"
    BLEND_MASK = "BlendMask"
    COND_INST = "CondInst"
    YOLACT = "YOLACT"

    def __init__(self, cView, model, conf):
        self.conf = conf
        self.conf.read("configuration/config.ini")
        self.cView = cView
        self.segmentationStarted = False

        self.pbar = QProgressBar()
        self.pbar.setValue(0)
        self.pbar.hide()        

        self.uploadVideoButton = QPushButton("")
        self.uploadVideoButton.clicked.connect(self.uploadVideoButtonCliked)
        self.uploadVideoButton.setIcon(QtGui.QIcon(self.conf.get("paths", "image")))
        self.uploadVideoButton.setStyleSheet("background:"+self.BUTTON_COLOR)
        self.uploadVideoButton.setMaximumHeight(22)

        self.textBoxVideoPath =  QLabel(self.CHANGE_VIDEO)
        self.textBoxVideoPath.setAlignment(QtCore.Qt.AlignCenter)

        layout = QGridLayout()
        layout.addWidget(self.textBoxVideoPath,0,0,1,4)
        layout.addWidget(self.uploadVideoButton,0,4,1,1)
        self.widgetUploadVideo = QWidget()
        self.widgetUploadVideo.setLayout(layout)

        self.startButton = QPushButton(self.START)
        self.startButton.clicked.connect(self.startButtonClicked)
        self.startButton.setStyleSheet("background:"+self.BUTTON_COLOR)

        self.textBoxSelectionHeader = QLabel(self.CHANGE_SYSTEM)
        self.textBoxSelectionHeader.setAlignment(QtCore.Qt.AlignHCenter)
        
        self.firstRadioButton = QRadioButton(self.BLEND_MASK)
        self.firstRadioButton.setChecked(True)
        self.secondRadioButton = QRadioButton(self.COND_INST)
        self.thirdRadioButton = QRadioButton(self.YOLACT)

        layout = QGridLayout()
        layout.addWidget(self.firstRadioButton,1,0,1,1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.secondRadioButton,2,0,1,1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.thirdRadioButton,3,0,1,1, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.startButton,4,0,1,1, Qt.AlignmentFlag.AlignCenter)
        self.widgetRadioButton = QWidget()
        self.widgetRadioButton.setLayout(layout)

        self.buttonGroup = QButtonGroup()
        self.buttonGroup.addButton(self.firstRadioButton)
        self.buttonGroup.addButton(self.secondRadioButton)
        self.buttonGroup.addButton(self.thirdRadioButton)
        self.buttonGroup.buttonClicked.connect(self._on_radio_button_clicked)

        self.leftMediaplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.leftVideoWidget = QVideoWidget()
        self.leftVideoWidget.setStyleSheet("background:"+self.FRAME_COLOR)
        self.leftMediaplayerWidget = QWidget() 
        self.leftMediaplayerWidget.setFixedWidth(800)
        self.leftMediaplayerWidget.setFixedHeight(400)
        self.textBoxLeftVideoName = QLabel("")

        layout = QGridLayout()
        layout.addWidget(self.leftVideoWidget,0,0,6,6)
        layout.addWidget(self.textBoxLeftVideoName,6,0,1,6,Qt.AlignmentFlag.AlignCenter)
        self.leftMediaplayerWidget.setLayout(layout)
        self.leftMediaplayer.setVideoOutput(self.leftVideoWidget)

        self.rightMediaplayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.rightVideoWidget = QVideoWidget()
        self.rightVideoWidget.setStyleSheet("background:"+self.FRAME_COLOR)
        self.rightMediaplayerWidget = QWidget()
        self.rightMediaplayerWidget.setFixedWidth(800)
        self.rightMediaplayerWidget.setFixedHeight(400)
        self.textBoxRightVideoName = QLabel("")

        layout = QGridLayout()
        layout.addWidget(self.rightVideoWidget,0,0,6,6)
        layout.addWidget(self.textBoxRightVideoName,6,0,1,6,Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.pbar,0,0,6,6)
        self.rightMediaplayerWidget.setLayout(layout)
        self.rightMediaplayer.setVideoOutput(self.rightVideoWidget)

        self.textBoxForFrameCount = QLabel("")
        self.textBoxForFrameCount.setAlignment(QtCore.Qt.AlignHCenter)
        self.textBoxForTime = QLabel("")
        self.textBoxForTime.setAlignment(QtCore.Qt.AlignHCenter)
        
        self.textBoxForRunningSystems = QLabel("")
        self.textBoxForRunningSystems.setAlignment(QtCore.Qt.AlignHCenter)

        self.nameOfSystemSegmentation = self.BLEND_MASK
        self.mPresenter =  MainPresenter(self,self.cView, model)

    def uploadVideoButtonCliked(self):
        self.runDefaultState()
        self.mPresenter.onUploadVideoButtonClick()
            
    def _on_radio_button_clicked(self, button):
        button.setChecked(True)
        self.nameOfSystemSegmentation = button.text()

    def startButtonClicked(self):
        if(self.textBoxVideoPath.text()== self.CHANGE_VIDEO):
            warningMessage = QMessageBox()
            warningMessage.setWindowTitle(self.WARNING)
            warningMessage.setText(self. WARNING_NOT_VIDEO)
            warningMessage.setIcon(QMessageBox.Warning)
            warningMessage.setStandardButtons(QMessageBox.Close)
            warningMessage.exec_()
        elif(not self.segmentationStarted):   
            self.mPresenter.onStartButtonClick(self.nameOfSystemSegmentation)
            self.segmentationStarted = True
            self.cView.segmentationStarted = True
        else:
            warningMessage = QMessageBox()
            warningMessage.setWindowTitle(self.WARNING)
            warningMessage.setText(self.WARNING_RESTART)
            warningMessage.setIcon(QMessageBox.Warning)
            warningMessage.setStandardButtons(QMessageBox.Close)
            warningMessage.exec_()
    
    def runDefaultState(self):
        self.segmentationStarted = False
        self.textBoxForRunningSystems.setText("")
        self.textBoxLeftVideoName.setText("")
        self.textBoxRightVideoName.setText("")
        self.textBoxForFrameCount.setText("")
        self.textBoxForTime.setText("")
        self.mPresenter.runningSystemsSet.clear()
        self.cView.runDefaultState()
        self.rightVideoWidget.update()
       
