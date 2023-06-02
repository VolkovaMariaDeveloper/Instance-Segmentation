from source.model.segmentation.ISegmentation import ISegmentation
import subprocess
import threading as th
import time
from subprocess import PIPE, run
import warnings
import os

class BlendMask(ISegmentation):
    LOG_FILE ="/home/mary/application/Instance-Segmentation/source/test.log"

    def __init__(self,videoPath, mPresenter):
        self.name = "BlendMask"
        self.videoPath = videoPath
        self.mPresenter = mPresenter
        self.persent = "0"
        self.averageFPS = 0.0
        self.time=""
        self.frameCount = ""



    def cmd(self):
        comand = "python ~/application/Instance-Segmentation/AdelaiDet/demo/demo.py \
    --config-file ~/application/Instance-Segmentation/AdelaiDet/configs/BlendMask/DLA_34_syncbn_4x.yaml \
    --video-input " + self.videoPath + " \
    --output ~/application/Instance-Segmentation/data/output/BlendMask \
    --confidence-threshold 0.35 \
    --opts MODEL.WEIGHTS ~/application/Instance-Segmentation/AdelaiDet/training_dir/DLA_34_syncbn_4x.pth "
        activateEnv = '. $CONDA_PREFIX/etc/profile.d/conda.sh && conda activate adelai-det &&'
        with open(self.LOG_FILE, "w+") as file:
            result = subprocess.run(activateEnv + comand,stdout=PIPE, stderr=file, universal_newlines=True, shell = True)

    def parseToGetPercent(self,string):
        str = ""
        for i in string:
            if (i =="%"):
                return str
            else:
                str+=i

    def passValues(self):
        while (self.persent!="100"):
            persent = self.persent
            if (persent==None):
                persent = 0
            self.mPresenter.changeValuePbar(int(persent))
            time.sleep(0.2)
        self.mPresenter.changeValuePbar(int(persent))       
        self.mPresenter.addFPSinResult(str(self.averageFPS),self.frameCount,self.time)
        self.mPresenter.hidePbar()

    def getCoutnFrames(self):
        with open(self.LOG_FILE, "r") as file:
            str = file.readlines()[-1]
            n = 26
            char = str[len(str)-n]
            while(char.isnumeric()):
                self.frameCount = char + self.frameCount
                n+=1
                char = str[len(str)-n] 


    def parseToGetFPS(self,str):
        fps = str[len(str)-9]+str[len(str)-8]+str[len(str)-7]+str[len(str)-6]
        return fps

    def getPersentAndAveFPS(self):
        start = time.time()
        count =0
        sum=0
        while (self.persent!="100"):
            with open(self.LOG_FILE, "r") as file:
                if(os.path.getsize(self.LOG_FILE)!=0):
                    str = file.readlines()[-1]
                    self.persent = self.parseToGetPercent(str)
                    if(self.persent!= None and self.persent.isnumeric()):
                        fps = float(self.parseToGetFPS(str))
                        count+=1
                        sum +=fps
        self.averageFPS=sum/count
        self.getCoutnFrames()
        self.time = time.time() - start
                

    def test(self,videoPath):
        
        threads = []
        threads.append(th.Thread(target=self.cmd))
        threads.append(th.Thread(target=self.getPersentAndAveFPS))
        threads.append(th.Thread(target=self.passValues))
 
        for i in threads:
            i.start()
        self.mPresenter.showPbar()