from presenter.IPresenter import IPresenter
from os import path
import time

class MainPresenter(IPresenter):


    def __init__(self, mView,cView, model):
        self.mView = mView
        self.cView = cView
        self.model = model
        self.runningSystemsSet = set()
        self.systemName = ""
        self.shortVideoName = ""

    def getShortPathName(self,full_name):
        listName = full_name.split(path.sep)
        return path.join("~ ../",listName[-4],listName[-3],listName[-2],listName[-1])

    def onUploadVideoButtonClick(self):
        pathVideo, self.shortVideoName = self.model.uploadVideo()
        self.mView.runVideo(pathVideo, self.mView.leftMediaplayer)
        self.mView.displayText(self.getShortPathName(pathVideo),self.mView.textBoxVideoPath)
        self.mView.displayText(self.shortVideoName, self.mView.textBoxLeftVideoName)

    def checkRunningSystems(self,systemName):
        self.runningSystemsSet.add(systemName)
        string = ', '.join(self.runningSystemsSet)
        return string

    def runSegmentedResults(self):
        videoPath = self.model.resultDictionary.get(self.systemName+"_videoPath")
        self.mView.runVideo(videoPath, self.mView.rightMediaplayer)
        self.mView.displayText(self.shortVideoName, self.mView.textBoxRightVideoName)
        self.mView.displayText(self.model.parseFrameCount(self.systemName), self.mView.textBoxForFrameCount)
        self.mView.displayText(self.model.parseTime(self.systemName), self.mView.textBoxForTime)

    def hidePbar(self):
        time.sleep(1.2)   
        self.mView.pbar.hide()
        self.mView.pbar.setValue(0)
        self.runSegmentedResults()
        self.mView.segmentationStarted = False
        self.cView.segmentationStarted = False

    def addResult(self,value,frameCount,time):
        self.model.resultDictionary[self.systemName+"_FPS"] = value
        self.model.resultDictionary[self.systemName+"_frameCount"] = frameCount
        self.model.resultDictionary[self.systemName+"_time"] = time

    def showPbar(self):
        self.mView.pbar.show()

    def changeValuePbar(self, value):
        self.mView.pbar.setValue(value)

    def onStartButtonClick(self, systemName):
        self.systemName = systemName
        resultDict = self.model.runSegmentation(self, systemName)
       
        systemsName = self.checkRunningSystems(systemName)
        self.mView.displayText(systemsName, self.mView.textBoxForRunningSystems)

        if (self.cView.leftComboBox.findText(systemName)==-1):
            self.cView.leftComboBox.addItem(systemName)
            self.cView.rightComboBox.addItem(systemName)
