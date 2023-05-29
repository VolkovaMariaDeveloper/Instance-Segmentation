from source.model.segmentation.ISegmentation import ISegmentation
import subprocess
import os
from subprocess import PIPE, run

class BlendMask(ISegmentation):
   
    def __init__(self):
        self.name = "BlendMask"

    def test(self):
        return "/home/mary/video/output/BlendMask/kiss.mkv"
    def test2(self,videoPath):
        command = "python ~/AdelaiDet/demo/demo.py \
    --config-file ~/AdelaiDet/configs/BlendMask/DLA_34_syncbn_4x.yaml \
    --video-input " + videoPath + " \
    --output ~/video/output/BlendMask \
    --confidence-threshold 0.35 \
    --opts MODEL.WEIGHTS ~/AdelaiDet/training_dir/DLA_34_syncbn_4x.pth "
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        print (result.returncode, result.stdout, result.stderr)