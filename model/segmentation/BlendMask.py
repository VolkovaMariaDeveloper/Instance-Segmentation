from model.segmentation.ISegmentation import ISegmentation
import subprocess
import os

class BlendMask(ISegmentation):
   
    def __init__(self):
        self.name = "BlendMask"

    def test2(self):
        return "/home/mary/video/output/BlendMask/kiss.mkv"
    def test(self,videoPath):
       # os.system("source ~/anaconda3/etc/profile.d/conda.sh")
       # os.system("conda activate blend-mask")
        os.system("python ~/AdelaiDet/demo/demo.py \
    --config-file ~/AdelaiDet/configs/BlendMask/DLA_34_syncbn_4x.yaml \
    --video-input " + videoPath + " \\" #~/video/input/#kiss.mp4\
    "--output ~/video/output/BlendMask \
    --confidence-threshold 0.35 \
    --opts MODEL.WEIGHTS ~/AdelaiDet/training_dir/DLA_34_syncbn_4x.pth ")
    #передать сообщение о том, что сохранение прошло успешно
        print("Success")
