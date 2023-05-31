from source.model.wrapper.Wrapper import Wrapper
from source.presenter.IPresenter import IPresenter
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

class MainPresenter(IPresenter):


    def __init__(self, mView,cView, model):
        self.mView = mView
        self.cView = cView
        self.model = model
        self.runningSystemsSet = set()
        self.nameSystemSegmentation = ""
        self.shortVideoName = "kiss"

    def onUploadVideoButtonClick(self):
        pathVideo, self.shortVideoName = self.model.uploadVideo()
        self.mView.runVideo(pathVideo, self.mView.leftMediaplayer)
        self.mView.displayText("~/application/source/data/output",self.mView.textBoxVideoPath)
        self.mView.displayText(self.shortVideoName, self.mView.textBoxLeftVideoName)

    def onUploadLabelButtonClick(self):
        shortLabelName = self.model.uploadLabel()
        self.mView.displayText(shortLabelName,self.mView.textBoxLabelName)

    def checkRunningSystems(self,systemName):
        self.runningSystemsSet.add(systemName)
        string = ', '.join(self.runningSystemsSet)
        return string

#TODO добавить результаты

    def parseTextResults(self):
        textResult = "Results: \n\n"
        fps = self.model.resultDictionary.get(self.nameSystemSegmentation+"_FPS")
        textResult+= "FPS: " + fps
        return textResult


    def runSegmentedResults(self):
        videoPath = self.model.resultDictionary.get(self.nameSystemSegmentation+"_videoPath")
        self.mView.runVideo(videoPath, self.mView.rightMediaplayer)
        self.mView.displayText(self.shortVideoName, self.mView.textBoxRightVideoName)
        self.mView.displayText(self.parseTextResults(), self.mView.textBoxForResults)



    def hidePbar(self):
        self.mView.pbar.hide()
        self.runSegmentedResults()


    def addFPSinResult(self,value):
        self.model.resultDictionary[self.nameSystemSegmentation+"_FPS"] = value

    def showPbar(self):
        self.mView.pbar.show()


    def changeValuePbar(self, value):
        self.mView.pbar.setValue(value)

    def onStartButtonClick(self, nameSystemSegmentation):
        self.nameSystemSegmentation = nameSystemSegmentation
        resultDict = self.model.runSegmentation(self, nameSystemSegmentation)
        systemsName = self.checkRunningSystems(nameSystemSegmentation)
        self.mView.displayText(systemsName, self.mView.textBoxForRunningSystems)

        if (self.cView.leftComboBox.findText(nameSystemSegmentation)==-1):
            self.cView.leftComboBox.addItem(nameSystemSegmentation)
            self.cView.rightComboBox.addItem(nameSystemSegmentation)

        
        #segmentatedVideoPath, shortSegmentedVideoName, quantitativeResults = self.model.runSegmentation(nameSystemSegmentation)
        #self.mView.runVideo(segmentatedVideoPath, self.mView.rightMediaplayer)
        #self.mView.displayText(shortSegmentedVideoName, self.mView.textBoxRightVideoName)
       #self.mView.displayText(quantitativeResults, self.mView.textBoxForResults)# возможно придется создать функцию, которая к приемлемому виду приведет результаты
       # self.mView.displayText(nameSystemSegmentation, self.mView.TextBoxForRunningSystems)
       # self.cView.addSystemForComparation(nameSystemSegmentation)

