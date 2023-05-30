from abc import ABC
from source.model.segmentation.ISegmentation import ISegmentation
from source.model.segmentation.BlendMask import BlendMask
from source.model.segmentation.CondInst import CondInst
from source.model.segmentation.YOLACT import YOLACT
from source.model.date_base.ITextData import ITextData
from source.model.date_base.IVideoData import IVideoData
from PyQt5.QtWidgets import QFileDialog
from os import path
import pathlib
from pathlib import Path

class Wrapper(IVideoData,ITextData):
    def __init__(self):
        self.labelPath = ""
        self.videoPath= "~/application/Instance-Segmentation/data/input/short.mp4"
        self.segmentationSystem = ISegmentation()#PolarMask(self.videoPath)
        self.segmentatedVideoPath = ""
        self.mainDirectory = ""
        self.nameVideo = ""
        self.resultDictionary = {}
        
    def getShortFileName(self,full_name):
        full_name = path.basename(full_name)
        name = path.splitext(full_name)[0]
        return name
  
    def uploadVideo(self):
        self.resultDictionary.clear()
        self.videoPath, _ = QFileDialog.getOpenFileName(None, "Upload Video")#, QDir.homePath())
        shortName = self.getShortFileName(self.videoPath)
        self.nameVideo = shortName
        path = Path(self.videoPath)
        pathsList = list(path.parents)
        self.mainDirectory = pathsList[1] #сохраняется путь к главной директории с папками Video, Labels,SegmentedVideos
        return self.videoPath, shortName

    def uploadLabel(self):
        self.labelPath, _ = QFileDialog.getOpenFileName(None, "Upload Video Label")
        #shortLabelName = self.getShortFileName(self.labelPath)
        return self.labelPath

    def createOutputPath(self):
        path = "/home/mary/video/output/" + self.segmentationSystem.name +"/"+ self.nameVideo+".mkv"
        return path

    def runSegmentation(self, segmentationSystemName):
        if segmentationSystemName == "BlendMask":
            self.segmentationSystem = BlendMask()
        elif segmentationSystemName == "CondInst":
            self.segmentationSystem = CondInst(self.videoPath)
        elif segmentationSystemName == "YOLACT":
            self.segmentationSystem = YOLACT()
            #quantitativeResults - словарь {FPS: значение, numberOfObjects: значение, IoU: значение}
        self.segmentationSystem.test(self.videoPath) 
        # возможно есть смысл системе сегментации возвращать путь к сохраненному видео
        # запуск сегментации определенной системы, если будут метки, то здесь их принимаем и записываем в словарь
        print(segmentationSystemName + "_videoPath")
        self.resultDictionary[segmentationSystemName + "_videoPath"] = self.createOutputPath() 

        return self.resultDictionary
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
    def searchResultsInTextFile(self):
        file = open(self.mainDirectory + "result/result.txt")
        dictionary = file.read()
        return dictionary  


