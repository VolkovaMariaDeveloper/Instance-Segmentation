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
    LOG_FILE ="/home/mary/application/Instance-Segmentation/source/test.log"
    
    def __init__(self,videoPath, mPresenter):
        self.name = "CondInst"
        self.argumentsDictionary ={} #возможно его следует создавать не здесь
        self.videoPath = videoPath
        self.anyObjects = AnyObjects()
        self.mPresenter = mPresenter
        self.persent = "0"
        self.averageFPS = 0.0

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
        with open(self.LOG_FILE, "w+") as file:
            result = subprocess.run(activateEnv + comand,stdout=PIPE, stderr=file, universal_newlines=True, shell = True)

    def parsingString(self,string):
        str = ""
        for i in string:
            if (i =="%"):
                return str
            else:
                str+=i

    def getSignal(self):
        while (self.persent!="100"):
            persent = self.persent
            if (persent==None):
                persent = 0
            self.mPresenter.changeValuePbar(int(persent))
            time.sleep(0.2)
        self.mPresenter.changeValuePbar(int(persent))
        time.sleep(0.2)
        self.mPresenter.addFPSinResult(str(self.averageFPS))
        self.mPresenter.hidePbar()

    def getFps(self,str):
        
        fps = str[len(str)-9]+str[len(str)-8]+str[len(str)-7]+str[len(str)-6]
        return fps

                


    def printpipe(self):
        count =0
        sum=0
        while (self.persent!="100"):
            with open(self.LOG_FILE, "r") as file:
                if(os.path.getsize(self.LOG_FILE)!=0):
                    str = file.readlines()[-1]
                    self.persent = self.parsingString(str)
                    if(self.persent!= None and self.persent.isnumeric()):
                        fps = float(self.getFps(str))
                        count+=1
                        sum +=fps
        self.averageFPS=sum/count
                


    def test(self,videoPath):
        
        #self.anyObjects.changed_value.connect(self.mPresenter.changeValuePbar)#функция из presentor
        threads = []
        threads.append(th.Thread(target=self.cmd))
        threads.append(th.Thread(target=self.printpipe))
        threads.append(th.Thread(target=self.getSignal))
 
        for i in threads:
            i.start()
            #time.sleep(5)
        self.mPresenter.showPbar()
        
        #print(result.stderr)
       # print(result.stdout)
        
