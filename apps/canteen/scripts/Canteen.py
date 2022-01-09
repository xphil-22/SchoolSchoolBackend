from canteen.scripts import Week, WebsiteGraber

class Canteen:
    def __init__(self, url:str="https://www.swfr.de/essen-trinken/speiseplaene/mensa-institutsviertel/"): #url std->Mensa Url <<constructor>>
        self._url = url
        self._graber = WebsiteGraber.WebsiteGraber(self._url) 
        self._graber.downloadWebsite() #Download HTML Code
    
    def getWeekMeals(self):
        currentWeek = Week.Week(html=self._graber.getWebsite()) #Create new Week with HTML etree object as Parameter
        return currentWeek.getWeekMeals() #call method getWeekMeals of currentWeek 
    
    def getTodaysMeal(self):
        todaysMeal = Week.Week(html=self._graber.getWebsite())
        return todaysMeal.getTodaysMeal()