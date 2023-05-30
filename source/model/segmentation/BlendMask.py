from source.model.segmentation.ISegmentation import ISegmentation
import subprocess
import os
from subprocess import PIPE, run

class BlendMask(ISegmentation):
   
    def __init__(self):
        self.name = "BlendMask"

    def test2(self):
        return "/home/mary/video/output/BlendMask/kiss.mkv"
    def test(self,videoPath):
        comand = "python ~/application/Instance-Segmentation/AdelaiDet/demo/demo.py \
    --config-file ~/application/Instance-Segmentation/AdelaiDet/configs/BlendMask/DLA_34_syncbn_4x.yaml \
    --video-input " + videoPath + " \
    --output ~/application/Instance-Segmentation/data/output/BlendMask \
    --confidence-threshold 0.35 \
    --opts MODEL.WEIGHTS ~/application/Instance-Segmentation/AdelaiDet/training_dir/DLA_34_syncbn_4x.pth "
        #comand_test = 'echo $CONDA_DEFAULT_ENV'
        result = subprocess.run('. $CONDA_PREFIX/etc/profile.d/conda.sh && conda activate adelai-det &&' + comand,stdout=PIPE, stderr=PIPE, universal_newlines=True, shell = True)
        #subprocess.run('bash -c "source activate adelai-det" &&' + comand_test, shell = True) 
        #subprocess.run('. /home/mary/miniconda3/bin/activate adelai-det &&' + conmand_test, shell = True) 
        #result = subprocess.run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        #print (result.returncode, result.stdout, result.stderr)
       # print("_______________________________________________________________________________________________________________")
        #print(result.returncode)
       # print("_______________________________________________________________________________________________________________")
        print(result.stdout)
        print("_______________________________________________________________________________________________________________")
        print(result.stderr)
       # print("_______________________________________________________________________________________________________________")
#