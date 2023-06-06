from abc import ABC,  abstractmethod

class IVideoData(ABC):
    @abstractmethod
    def uploadVideo():
        pass