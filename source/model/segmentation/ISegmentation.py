from abc import ABC

class ISegmentation(ABC):
    def segmentation(self):
        pass
    def test(self):
        return "ISegmentation"
