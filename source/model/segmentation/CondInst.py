from source.model.segmentation.ISegmentation import ISegmentation
import subprocess 
import threading as th
import time
from subprocess import PIPE, run
import warnings
import os


class CondInst(ISegmentation):
    CONFIG_FILE = "configs/CondInst/MS_R_50_BiFPN_3x_sem.yaml"
    OUTPUT_PATH = "~/video/output/CondInst"
    MODEL_WEIGHTS = "training_dir/CondInst_MS_R_50_BiFPN_3x_sem.pth"
    CONFIDENCE_THRESHOLD = 0.35
    def __init__(self,videoPath):
        self.name = "CondInst"
        self.argumentsDictionary ={} #возможно его следует создавать не здесь
        self.videoPath = videoPath
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
                #fillFile = file.read()
                persent = self.parsingString(file.readlines()[-1])
                print(persent)#.decode('cp1251'))
                time.sleep(1)


    def test(self,videoPath):
        
        threads = []
        threads.append(th.Thread(target=self.cmd))
        threads.append(th.Thread(target=self.printpipe))
 
        for i in threads:
            i.start()
            time.sleep(3)
        #print(result.stderr)
       # print(result.stdout)
        
