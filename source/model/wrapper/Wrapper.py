from model.segmentation.ISegmentation import ISegmentation
from model.segmentation.BlendMask import BlendMask
from model.segmentation.CondInst import CondInst
from model.segmentation.YOLACT import YOLACT

from model.date_base.IVideoData import IVideoData
from PyQt5.QtWidgets import QFileDialog
from os import path
from pathlib import Path
import math 

class Wrapper(IVideoData):
    TITLE = "Загрузка видео"
    def __init__(self,conf):
        self.conf = conf
        self.conf.read("configuration/config.ini")
        self.videoPath= ""
        self.segmentationSystem = ISegmentation()
        self.nameVideo = ""
        self.resultDictionary = {}
        
    def getShortFileName(self,fullName):
        fullName = path.basename(fullName)
        name = path.splitext(fullName)[0]
        return name
  
    def uploadVideo(self):
        self.resultDictionary.clear()
        self.videoPath, _ = QFileDialog.getOpenFileName(None, self.TITLE, self.conf.get("paths", "data"))
        shortName = self.getShortFileName(self.videoPath)
        self.nameVideo = shortName
        return self.videoPath, shortName

    def createOutputPath(self):
        path = self.conf.get("paths", "fill_out") + self.segmentationSystem.name +"/"+ self.nameVideo+".mp4"
        return path

    def parseFrameCount(self, nameSystemSegmentation):
        frameCount = self.resultDictionary.get(nameSystemSegmentation +"_frameCount")
        textResult = "Количество кадров: " + frameCount +"\n"
        return textResult
    
    def parseTime(self, nameSystemSegmentation):
        fps = self.resultDictionary.get(nameSystemSegmentation +"_FPS")
        time = self.resultDictionary.get(nameSystemSegmentation +"_time")
        textResult= "FPS: " + fps +"\n"
        textResult+= "Время сегментации: " + str(round(time)) +" c\n"
        return textResult

    def runSegmentation(self, mPresenter, segmentationSystemName):
        if segmentationSystemName == "BlendMask":
            self.segmentationSystem = BlendMask(self.videoPath, mPresenter, self.conf)
        elif segmentationSystemName == "CondInst":
            self.segmentationSystem = CondInst(self.videoPath, mPresenter, self.conf)
        elif segmentationSystemName == "YOLACT":
            self.segmentationSystem = YOLACT(self.videoPath, mPresenter, self.conf)
        self.segmentationSystem.segmentation() 
        self.resultDictionary[segmentationSystemName + "_videoPath"] = self.createOutputPath() 
        return self.resultDictionary
       


