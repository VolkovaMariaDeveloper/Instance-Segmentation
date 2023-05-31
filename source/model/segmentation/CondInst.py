from source.model.segmentation.ISegmentation import ISegmentation
import subprocess 
import threading as th
import time
from subprocess import PIPE, run
import warnings
import os
from PyQt5.QtCore import Qt, pyqtSignal, QObject


class AnyObjects(QObject):
    changed_value = pyqtSignal(int)


class CondInst(ISegmentation):
    CONFIG_FILE = "configs/CondInst/MS_R_50_BiFPN_3x_sem.yaml"
    OUTPUT_PATH = "~/video/output/CondInst"
    MODEL_WEIGHTS = "training_dir/CondInst_MS_R_50_BiFPN_3x_sem.pth"
    CONFIDENCE_THRESHOLD = 0.35
    
    def __init__(self,videoPath, mPresenter):
        self.name = "CondInst"
        self.argumentsDictionary ={} #возможно его следует создавать не здесь
        self.videoPath = videoPath
        self.anyObjects = AnyObjects()
        self.mPresenter = mPresenter

    def segmentation(self, videoPath):
        self.argumentsDictionary["video_input"] = videoPath
        self.argumentsDictionary["config_file"] = self.CONFIG_FILE
        self.argumentsDictionary["output"] = self.OUTPUT_PATH
        self.argumentsDictionary["confidence_threshold"] = self.CONFIDENCE_THRESHOLD
        self.argumentsDictionary["opts"] = ["MODEL.WEIGHTS", self.MODEL_WEIGHTS]
       # demo.startDemo( self.argumentsDictionary)



        pass
    def cmd(self):

        comand = "python ~/application/Instance-Segmentation/AdelaiDet/demo/demo.py \
    --config-file ~/application/Instance-Segmentation/AdelaiDet/configs/CondInst/MS_R_50_BiFPN_3x_sem.yaml \
    --video-input " + self.videoPath + " \
    --output ~/application/Instance-Segmentation/data/output/CondInst \
    --confidence-threshold 0.35 \
    --opts MODEL.WEIGHTS ~/application/Instance-Segmentation/AdelaiDet/training_dir/CondInst_MS_R_50_BiFPN_3x_sem.pth "
        activateEnv = '. $CONDA_PREFIX/etc/profile.d/conda.sh && conda activate adelai-det &&'
        with open("/home/mary/application/Instance-Segmentation/source/test.log", "w+") as file:
            result = subprocess.run(activateEnv + comand,stdout=PIPE, stderr=file, universal_newlines=True, shell = True)

    def parsingString(self,string):
        
        str = ""
        for i in string:
            if (i =="%"):
                return str
            else:
                str+=i


    def printpipe(self):
        
        persent = ""
        while (persent!="100"):
            with open("/home/mary/application/Instance-Segmentation/source/test.log", "r") as file:
                persent = self.parsingString(file.readlines()[-1])
                print(persent)# передавать значения на Главную вкладку в отдельном потоке через презентер?
                self.anyObjects.changed_value.emit(int(persent))
                time.sleep(0.5)


    def test(self,videoPath):
        
        self.anyObjects.changed_value.connect(self.mPresenter.changeValuePbar)#функция из presentor
        threads = []
        threads.append(th.Thread(target=self.cmd))
        threads.append(th.Thread(target=self.printpipe))
 
        for i in threads:
            i.start()
            time.sleep(6)
        
        #print(result.stderr)
       # print(result.stdout)
        
