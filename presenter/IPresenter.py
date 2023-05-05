from abc import ABC, abstractmethod

class IPresenter(ABC):
    @abstractmethod
    def onStartButtonClick():
        pass
    @abstractmethod
    def onTabClick():
        pass