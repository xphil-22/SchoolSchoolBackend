from canteen.scripts import Week, WebsiteGraber

class Canteen:
    def __init__(self, url:str="https://www.swfr.de/essen-trinken/speiseplaene/mensa-institutsviertel/") -> None: #url=std->Mensa Url
        self._url:str = url
        self._graber:WebsiteGraber = WebsiteGraber.WebsiteGraber(self._url) 
        self._graber.downloadWebsite() #Download HTML Code
    
    def getWeekMeals(self) -> list[dict[str]]:
        currentWeek = Week.Week(html=self._graber.getWebsite()) #Create new Week with HTML etree object as Parameter
        return currentWeek.getWeekMeals() #call method getWeekMeals of currentWeek 
    
    def getTodaysMeal(self) -> list[dict[str]]:
        todaysMeal = Week.Week(html=self._graber.getWebsite()) #Create new Week with HTML etree object as Parameter
        return todaysMeal.getTodaysMeal() #call method getTodaysMeal of currentWeek 