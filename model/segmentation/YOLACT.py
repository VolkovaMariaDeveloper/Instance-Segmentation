from model.segmentation.ISegmentation import ISegmentation

class YOLACT(object):
    def __getattr__(self, item):
        return ISegmentation.__dict__[item]
    def __init__(self, videoPath):
        pass
    def segmentation():
        pass 
    def test(self):
        return "YOLACT"  