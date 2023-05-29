from abc import ABC, abstractmethod
from PyQt5.QtCore import  QUrl
from PyQt5.QtMultimedia import QMediaContent


class IView(ABC):
    def runVideo(self, path, mediaplayer):
        if path != '':
            mediaplayer.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
            mediaplayer.play()

    def displayText( self,text, textBox):
        textBox.setText(text)

    @abstractmethod
    def runDefaultState():
        pass