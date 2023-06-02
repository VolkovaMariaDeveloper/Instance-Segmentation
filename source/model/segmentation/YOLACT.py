from source.model.segmentation.ISegmentation import ISegmentation
import subprocess 
import threading as th
import time
from subprocess import PIPE, run
import warnings
import os

class YOLACT(ISegmentation):
    LOG_FILE ="/home/mary/application/Instance-Segmentation/source/test.log"
    def __init__(self,videoPath, mPresenter):
        self.name = "YOLACT"
        self.videoPath = videoPath
        self.mPresenter = mPresenter
        self.persent = "0"
        self.averageFPS = 0.0
        self.time=""
        self.frameCount = ""
        self.shortVideoName = self.mPresenter.shortVideoName
    def segmentation(videoPath):
        pass 
    def cmd(self):
        comand = 'python yolact_edge/eval.py \
        --trained_model=yolact_edge/weights/yolact_edge_vid_847_50000.pth \
        --score_threshold=0.3 \
        --top_k=100 \
        --video='+ self.videoPath +':data/output/YOLACT/'+self.shortVideoName+'.mp4 \
        --display_bboxes False \
        --disable_tensorrt '
        activateEnv = '. $CONDA_PREFIX/etc/profile.d/conda.sh && conda activate yolact-env &&'
        with open(self.LOG_FILE, "w+") as file:
            subprocess.run(activateEnv + comand, stdout=file,  universal_newlines=True, shell = True)


        
    def is_number(self,str):
        try:
            float(str)
            return True
        except ValueError:
            return False       

    def passValues(self):
        while (self.persent!="100.00"):
            persent = self.persent
            self.mPresenter.changeValuePbar(float(persent))
            time.sleep(0.2)
        self.mPresenter.changeValuePbar(float(persent))       
        self.mPresenter.addFPSinResult(str(self.averageFPS),self.frameCount,self.time)
        self.mPresenter.hidePbar()


    def parseString(self,str,signalChar, index):
        n = index
        fps = ""
        char = str[len(str)-n]
        while (char != signalChar):
            fps = char + fps
            n+=1
            char = str[len(str)-n]
        return n, fps


    def getPersentAndAveFPS(self):
        count =0
        sum=0
        start = time.time()
        while (self.persent!="100.00"):
            with open(self.LOG_FILE, "r") as file:
                if(os.path.getsize(self.LOG_FILE)!=0):
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
                

    def test(self,videoPath):
        threads = []
        threads.append(th.Thread(target=self.cmd))
        threads.append(th.Thread(target=self.getPersentAndAveFPS))
        threads.append(th.Thread(target=self.passValues))
 
        for i in threads:
            i.start()
        self.mPresenter.showPbar()
 