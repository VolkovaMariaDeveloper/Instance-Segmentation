from model.segmentation.ISegmentation import ISegmentation
import subprocess 
import threading as th
import time
from subprocess import PIPE, run
import warnings
import os

class YOLACT(ISegmentation):
    def __init__(self,videoPath, mPresenter, conf):
        self.conf = conf
        self.conf.read("configuration/config.ini")
        self.name = "YOLACT"
        self.videoPath = videoPath
        self.mPresenter = mPresenter
        self.persent = "0"
        self.averageFPS = 0.0
        self.time=""
        self.frameCount = ""
        self.shortVideoName = self.mPresenter.shortVideoName

    def runDemo(self):
        activateEnv = self.conf.get("command", "env_yolact")
        command = (self.conf.get("command", "segmentation_Yolact_first") 
                  + self.videoPath + self.conf.get("command", "segmentation_Yolact_second")
                  +self.shortVideoName + self.conf.get("command", "segmentation_Yolact_third"))
        with open(self.conf.get("paths", "log_file"), "w+") as file:
            subprocess.run(activateEnv + command, stdout=file,  universal_newlines=True, shell = True)      

    def passValues(self):
        while (self.persent!="100.00"):
            persent = self.persent
            self.mPresenter.changeValuePbar(float(persent))
        self.mPresenter.changeValuePbar(float(persent))  
        time.sleep(0.2)     
        self.mPresenter.addResult(str(self.averageFPS),self.frameCount,self.time)
        self.mPresenter.hidePbar()


    def parseString(self,str,signalChar, index):
        n = index
        value = ""
        char = str[len(str)-n]
        while (char != signalChar):
            value = char + value
            n+=1
            char = str[len(str)-n]
        return n, value


    def getPersentAndAveFPS(self):
        count =0
        sum=0
        start = time.time()
        while (self.persent!="100.00"):
            with open(self.conf.get("paths", "log_file"), "r") as file:
                if(os.path.getsize(self.conf.get("paths", "log_file"))!=0):
                    str = file.readlines()[-1]
                    str = str.replace(' ', '')
                    if(str.startswith('Processing')):
                        index_fps, fps = self.parseString(str,")",4)
                        index_persent, self.persent = self.parseString(str,"(",index_fps +2)
                        count+=1
                        sum +=float(fps[:-1])
        self.averageFPS=round(sum/count,2)
        _, self.frameCount = self.parseString(str,"/",index_persent +1)
        self.time = time.time() - start
                

    def segmentation(self):
        threads = []
        threads.append(th.Thread(target=self.runDemo))
        threads.append(th.Thread(target=self.getPersentAndAveFPS))
        threads.append(th.Thread(target=self.passValues))
 
        for i in threads:
            i.start()
        self.mPresenter.showPbar()
 