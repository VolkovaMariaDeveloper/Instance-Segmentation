from abc import ABC

from PyQt5.QtWidgets import QFileDialog
from os import path
import pathlib

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
        #shortLabelName = self.getShortFileName(self.labelPath)
        return self.labelPath

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


