from canteen.scripts import Week, WebsiteGraber

class Canteen:
    def __init__(self, url:str="https://www.swfr.de/essen-trinken/speiseplaene/mensa-institutsviertel/"):
        self._url = url
        self._graber = WebsiteGraber.WebsiteGraber(self._url)
        self._graber.downloadWebsite() 
    
    def getWeekMeals(self):
        currentWeek = Week.Week(html=self._graber.getWebsite())
        return currentWeek.getWeekMeals()
    
    def getTodaysMeal(self):
        todaysMeal = Week.Week(html=self._graber.getWebsite())
        return todaysMeal.getTodaysMeal()