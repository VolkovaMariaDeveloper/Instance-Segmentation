from source.model.segmentation.ISegmentation import ISegmentation


class CondInst(ISegmentation):
    CONFIG_FILE = "configs/CondInst/MS_R_50_BiFPN_3x_sem.yaml"
    OUTPUT_PATH = "~/video/output/CondInst"
    MODEL_WEIGHTS = "training_dir/CondInst_MS_R_50_BiFPN_3x_sem.pth"
    CONFIDENCE_THRESHOLD = 0.35
    def __init__(self):
        self.name = "CondInst"
        self.argumentsDictionary ={} #возможно его следует создавать не здесь
    def segmentation(self, videoPath):
        self.argumentsDictionary["video_input"] = videoPath
        self.argumentsDictionary["config_file"] = self.CONFIG_FILE
        self.argumentsDictionary["output"] = self.OUTPUT_PATH
        self.argumentsDictionary["confidence_threshold"] = self.CONFIDENCE_THRESHOLD
        self.argumentsDictionary["opts"] = ["MODEL.WEIGHTS", self.MODEL_WEIGHTS]
       # demo.startDemo( self.argumentsDictionary)



        pass
    def test(self,videoPath):
        return "/home/mary/video/output/BlendMask/kiss.mkv"

