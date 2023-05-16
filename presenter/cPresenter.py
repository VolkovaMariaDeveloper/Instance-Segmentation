from model.wrapper.Wrapper import Wrapper
from presenter.IPresenter import IPresenter

class ComparasionPresenter(IPresenter):


    def __init__(self, cView, model:Wrapper):
        self.cView = cView
        self.model = model# нужна модель из MainPresenter

    def getOutputResults(dictionary):
        stringOfResults = ""
        namesOfResults = dictionary.keys()
        namesOfResults.pop(0) # удаляем путь на сегментированное видео 
        for key in namesOfResults:
            stringOfResults += key + ": " + dictionary[key] +";\n"
        return stringOfResults

    def onStartButtonClick(self):
        #для выбранной левой системы
        resultDictionaryForLeftSystem = self.model.searchResultsInTextFile(self.cView.leftSystem) 
        self.cView.runVideo(resultDictionaryForLeftSystem["segmentedVideoPath"],self.cView.leftMediaplayer)
        #функция по преобразованию информации из словаря к читабельному виду
        outputResults = self.getOutputResults(resultDictionaryForLeftSystem)
        self.cView.displayText(outputResults, self.cView.leftTextBoxForResults)
        shortLeftVideoName = self.model.getShortFileName(resultDictionaryForLeftSystem["segmentedVideoPath"])
        self.cView.displayText(shortLeftVideoName, self.cView.TextBoxLeftVideoName)

        #для выбранной правой системы
        resultDictionaryForRightSystem = self.model.searchResultsInTextFile(self.cView.rightSystem) 
        self.cView.runVideo(resultDictionaryForRightSystem["segmentedVideoPath"], self.cView.rightMediaplayer)
        #функция по преобразованию информации из словаря к читабельному виду
        outputResults = self.getOutputResults(resultDictionaryForRightSystem)
        self.cView.displayText(outputResults, self.cView.rightTextBoxForResults)
        shortRightVideoName = self.model.getShortFileName(resultDictionaryForRightSystem["segmentedVideoPath"])
        self.cView.displayText(shortRightVideoName, self.cView.TextBoxRightVideoName)
        pass

    def onTabClick(self):
        pass  