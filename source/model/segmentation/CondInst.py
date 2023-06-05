from model.segmentation.ISegmentation import ISegmentation
import subprocess 
import threading as th
import time
from subprocess import PIPE, run
import os



class CondInst(ISegmentation):
    
    def __init__(self,videoPath, mPresenter, conf):
        self.conf = conf
        self.conf.read("configuration/config.ini")
        self.name = "CondInst"
        self.videoPath = videoPath
        self.mPresenter = mPresenter
        self.persent = "0"
        self.averageFPS = 0.0
        self.time=""
        self.frameCount = ""

    def cmd(self):
        activateEnv = self.conf.get("command", "env_adelai")
        command = (self.conf.get("command", "segmentation_CondInst_first") + " "
                  + self.videoPath +" "
                  + self.conf.get("command", "segmentation_CondInst_second"))
        with open(self.conf.get("paths", "log_file"), "w+") as file:
            subprocess.run(activateEnv + command,stdout=PIPE, stderr=file, universal_newlines=True, shell = True)

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
            if (persent!=None):
                self.mPresenter.changeValuePbar(int(persent))
        self.mPresenter.changeValuePbar(int(persent))  
        time.sleep(1)   
        self.mPresenter.addFPSinResult(str(self.averageFPS),self.frameCount,self.time)
        self.mPresenter.hidePbar()

    def getCoutnFrames(self):
        with open(self.conf.get("paths", "log_file"), "r") as file:
            str = file.readlines()[-1]
            n = 27
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
            with open(self.conf.get("paths", "log_file"), "r") as file:
                if(os.path.getsize(self.conf.get("paths", "log_file"))!=0):
                    str = file.readlines()[-1]
                    self.persent = self.parseToGetPercent(str)
                    fps = self.parseToGetFPS(str)
                    if(self.is_number(fps)):                       
                        count+=1
                        sum +=float(fps)
        self.averageFPS=round(sum/count,2)
        self.getCoutnFrames()
        self.time = time.time() - start

    def is_number(self,str):
        try:
            float(str)
            return True
        except ValueError:
            return False                  

    def segmentation(self):
        
        threads = []
        threads.append(th.Thread(target=self.cmd))
        threads.append(th.Thread(target=self.getPersentAndAveFPS))
        threads.append(th.Thread(target=self.passValues))
 
        for i in threads:
            i.start()
        self.mPresenter.showPbar()

        
