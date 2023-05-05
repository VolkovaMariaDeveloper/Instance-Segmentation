from model.segmentation.ISegmentation import ISegmentation

class BlendMask(object):
    def __getattr__(self, item):
        return ISegmentation.__dict__[item]
    def __init__(self, videoPath):
        pass
    def test(self):
        return "BlendMask"
