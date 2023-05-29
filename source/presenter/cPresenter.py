from source.model.wrapper.Wrapper import Wrapper
from source.presenter.IPresenter import IPresenter

class ComparasionPresenter(IPresenter):


    def __init__(self, cView, model:Wrapper):
        self.cView = cView
        self.model = model# нужна модель из MainPresenter

    def onStartButtonClick(self):
        #для выбранной левой системы
        leftSystem = self.cView.leftComboBox.currentText()
        videoPath = self.model.resultDictionary.get(leftSystem+"_videoPath") #создать текстовые константы
        self.cView.runVideo(videoPath,self.cView.leftMediaplayer)
        self.cView.displayText("6 FPS, 12 объектов", self.cView.textBoxForLeftResults)
        print(videoPath)
        shortLeftVideoName = self.model.getShortFileName(videoPath)
        self.cView.displayText("kiss_blend_mask", self.cView.textBoxLeftVideoName)
        self.cView.runVideo("D:\\University\\Magistracy\\Segmentation\\application\\source\\data\\output\\output_kiss_video.mp4", self.cView.leftMediaplayer)

        import time
        time.sleep(1)
        self.cView.runVideo("D:\\University\\Magistracy\\Segmentation\\application\\source\\data\\output\\output_kiss_video.mp4", self.cView.rightMediaplayer)
        #для выбранной правой системы
        rightSystem = self.cView.rightComboBox.currentText()
        videoPath = self.model.resultDictionary.get(rightSystem+"_videoPath")
       # self.cView.runVideo(videoPath, self.cView.rightMediaplayer)
        self.cView.displayText("4.7 FPS, 13 объектов", self.cView.textBoxForRightResults)
        shortRightVideoName = self.model.getShortFileName(videoPath)
        self.cView.displayText("kiss_cond_inst", self.cView.textBoxRightVideoName)

  