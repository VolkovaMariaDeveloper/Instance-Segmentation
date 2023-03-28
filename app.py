from abc import ABC, abstractmethod
from PyQt5.QtCore import QDir, QUrl
from PyQt5.QtWidgets import QHBoxLayout, QGridLayout,QComboBox, QPushButton,QRadioButton,QButtonGroup, QMainWindow,QTabWidget,QFileDialog, QLabel, QVBoxLayout, QWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import (QApplication)
from PyQt5.QtMultimediaWidgets import QVideoWidget
from os import path
import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
import pathlib

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
        #Добавить все визуальтые блоки в сетку предварительно создав виджеты для компановки элементов

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        




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

class IMainPresenter(ABC):
    @abstractmethod
    def onUploadVideoButtonClick():
        pass
    @abstractmethod
    def onUploadLabelButtonClick():
        pass
    @abstractmethod
    def onStartButtonClick():
        pass
    @abstractmethod
    def onTabClick():
        pass

class MainPresenter(IMainPresenter):
    def __init__(self, mView):#:MainView):не получается передать объет класса со всеми его атрибутами
        self.mView = mView

        self.model = Model()
        self.cView = ComparasionView(self.model)
        self.runningSystemsSet = set()

    def onUploadVideoButtonClick(self):
        pathVideo, shortVideoName = self.model.uploadVideo()
        self.mView.runVideo(pathVideo, self.mView.leftMediaplayer)
        self.mView.displayText(shortVideoName, self.mView.textBoxLeftVideoName)
        

    def onUploadLabelButtonClick(self):
        shortLabelName = self.model.uploadLabel()
        self.mView.displayText(shortLabelName,self.mView.textBoxLabelName)

    def checkRunningSystems(self,systemName):
        self.runningSystemsSet.add(systemName)
        string = ', '.join(self.runningSystemsSet)
        return string


    def onStartButtonClick(self, nameSystemSegmentation):
        testName = self.model.runSegmentation(nameSystemSegmentation)
        systemsName = self.checkRunningSystems(testName)
        self.mView.displayText(systemsName, self.mView.textBoxForRunningSystems)

        #self.cView.leftComboBox.addItem(testName)

        
        #segmentatedVideoPath, shortSegmentedVideoName, quantitativeResults = self.model.runSegmentation(nameSystemSegmentation)
        #self.mView.runVideo(segmentatedVideoPath, self.mView.rightMediaplayer)
        #self.mView.displayText(shortSegmentedVideoName, self.mView.textBoxRightVideoName)
       #self.mView.displayText(quantitativeResults, self.mView.textBoxForResults)# возможно придется создать функцию, которая к приемлемому виду приведет результаты
       # self.mView.displayText(nameSystemSegmentation, self.mView.TextBoxForRunningSystems)
       # self.cView.addSystemForComparation(nameSystemSegmentation)
        
    def onTabClick():
        pass

class IVideoData(ABC):
    def uploadVideo():
        pass
    def uploadLabel():
        pass
    def saveVideo():
        pass
    
class ITextData(ABC):
    def saveResultsInTextFile():
        pass
    def searchResultsInTextFile(systemName):
        pass

class ISegmentation(ABC):
    def segmentation():
        pass
    def test(self):
        return "ISegmentation"

class BlendMask(ISegmentation):
    def __init__(self, videoPath):
        pass
    def test(self):
        return "BlendMask"

class PolarMask(ISegmentation):
    def __init__(self, videoPath):
        pass
    def segmentation():
        pass
    def test(self):
        return "PolarMask"

class YOLACT(ISegmentation):
    def __init__(self, videoPath):
        pass
    def segmentation():
        pass 
    def test(self):
        return "YOLACT"  

class Model(IVideoData,ITextData):
    def __init__(self):
        self.labelPath = ""
        self.videoPath= ""
        self.segmentationSystem = ISegmentation()#PolarMask(self.videoPath)
        self.segmentatedVideoPath = ""
        self.mainDirectory = ""
        self.nameVideo = ""
        
    def getShortFileName(self,full_name):
        full_name = path.basename(full_name)
        name = path.splitext(full_name)[0]
        return name
  
    def uploadVideo(self):
        self.videoPath, _ = QFileDialog.getOpenFileName(None, "Upload Video")#, QDir.homePath())
        shortName = self.getShortFileName(self.videoPath)
        self.nameVideo = shortName
        path = pathlib.WindowsPath(self.videoPath)
        pathsList = list(path.parents)
        self.mainDirectory = pathsList[1] #сохраняется путь к главной директории с папками Video, Labels,SegmentedVideos
        return self.videoPath, shortName

    def uploadLabel(self):
        self.labelPath, _ = QFileDialog.getOpenFileName(None, "Upload Video Label")
        shortLabelName = self.getShortFileName(self.labelPath)
        return shortLabelName

    def runSegmentation(self, segmentationSystem):
        if segmentationSystem == "BlendMask":
            self.segmentationSystem = BlendMask(self.videoPath)
        elif segmentationSystem == "PolarMask":
            self.segmentationSystem = PolarMask(self.videoPath)
        elif segmentationSystem == "YOLACT":
            self.segmentationSystem = YOLACT(self.videoPath)
            #quantitativeResults - словарь {FPS: значение, numberOfObjects: значение, IoU: значение}
        stringName = self.segmentationSystem.test()
        return stringName
        #segmentedVideo, quantitativeResults = self.segmentationSystem.segmentation(self.videoPath, self.labelPath)
       # self.segmentatedVideoPath = self.saveVideo(segmentedVideo)
        #self.saveResultsInTextFile(quantitativeResults)
       # shortSegmentedVideoName = self.getShortFileName( self.segmentedVideoPath)
       # return self.segmentatedVideoPath, shortSegmentedVideoName, quantitativeResults
    
    #создается директория segmentedVideo, видео сохраняется по названию исходного видео+имя системы, возвращает ссылку на видео
    def saveVideo(segmentedVideo):
        pass

    def saveResultsInTextFile():# для каждого видеофайла создает отдельный текстовый файл с результатами систем в формате json[BlendMask:{путь к сегментированному видео +словарь результатов}, PolarMask, YOLACT]
        pass
    def searchResultsInTextFile():
        pass   

class IComparasionPresenter(ABC):
    @abstractmethod
    def onStartButtonClick():
        pass
    @abstractmethod
    def onTabClick():
        pass

class ComparasionPresenter(IComparasionPresenter):
    def __init__(self, cView:ComparasionView, model:Model):
        self.cView = cView
        self.model = model# нужна модель из MainPresenter

    def getOutputResults(dictionary):
        stringOfResults = ""
        namesOfResults = dictionary.keys()
        namesOfResults.pop(0) # удаляем путь на сегментированное видео 
        for key in namesOfResults:
            stringOfResults += key + ": " + dictionary[key] +";\n"
        return stringOfResults

    def onStartButtonClick(self):
        #для выбранной левой системы
        resultDictionaryForLeftSystem = self.model.searchResultsInTextFile(self.cView.leftSystem) 
        self.cView.runVideo(resultDictionaryForLeftSystem["segmentedVideoPath"],self.cView.leftMediaplayer)
        #функция по преобразованию информации из словаря к читабельному виду
        outputResults = self.getOutputResults(resultDictionaryForLeftSystem)
        self.cView.displayText(outputResults, self.cView.leftTextBoxForResults)
        shortLeftVideoName = self.model.getShortFileName(resultDictionaryForLeftSystem["segmentedVideoPath"])
        self.cView.displayText(shortLeftVideoName, self.cView.TextBoxLeftVideoName)

        #для выбранной правой системы
        resultDictionaryForRightSystem = self.model.searchResultsInTextFile(self.cView.rightSystem) 
        self.cView.runVideo(resultDictionaryForRightSystem["segmentedVideoPath"], self.cView.rightMediaplayer)
        #функция по преобразованию информации из словаря к читабельному виду
        outputResults = self.getOutputResults(resultDictionaryForRightSystem)
        self.cView.displayText(outputResults, self.cView.rightTextBoxForResults)
        shortRightVideoName = self.model.getShortFileName(resultDictionaryForRightSystem["segmentedVideoPath"])
        self.cView.displayText(shortRightVideoName, self.cView.TextBoxRightVideoName)
        pass

    def onTabClick(self):
        pass  
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())


