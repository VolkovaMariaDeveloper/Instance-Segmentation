from model.wrapper.Wrapper import Wrapper
from presenter.IPresenter import IPresenter

class MainPresenter(IPresenter):


    def __init__(self, mView,cView):#:MainView):не получается передать объет класса со всеми его атрибутами
        self.mView = mView
        self.cView = cView
        self.model = Wrapper()
        #self.cView = ComparasionView(self.model)
        self.runningSystemsSet = set()

    def onUploadVideoButtonClick(self):
        pathVideo, shortVideoName = self.model.uploadVideo()
        self.mView.runVideo(pathVideo, self.mView.leftMediaplayer)
        self.mView.displayText(pathVideo,self.mView.textBoxVideoPath)
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
#!!!!Сделать проверку на уникальность
        self.cView.leftComboBox.addItem(testName)
        self.cView.rightComboBox.addItem(testName)

        
        #segmentatedVideoPath, shortSegmentedVideoName, quantitativeResults = self.model.runSegmentation(nameSystemSegmentation)
        #self.mView.runVideo(segmentatedVideoPath, self.mView.rightMediaplayer)
        #self.mView.displayText(shortSegmentedVideoName, self.mView.textBoxRightVideoName)
       #self.mView.displayText(quantitativeResults, self.mView.textBoxForResults)# возможно придется создать функцию, которая к приемлемому виду приведет результаты
       # self.mView.displayText(nameSystemSegmentation, self.mView.TextBoxForRunningSystems)
       # self.cView.addSystemForComparation(nameSystemSegmentation)
        
    def onTabClick():
        pass
