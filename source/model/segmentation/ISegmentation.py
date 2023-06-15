from abc import ABC, abstractmethod

class ISegmentation(ABC):

    def segmentation():
        pass
    def runDemo():
        pass

    def isNumber(self,str):
        try:
            float(str)
            return True
        except ValueError:
            return False     
