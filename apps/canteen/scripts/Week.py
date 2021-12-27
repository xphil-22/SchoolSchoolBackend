from canteen.scripts.Day import Day
import datetime

class Week:
    def __init__(self, html):
        self._days = []
        self._day_acronyms = ['mon','tue','wed','thu','fri']
        
        for day_acronym in self._day_acronyms:
            day_data = html.xpath(f"//*[@id=\"tab-{day_acronym}\"]")[0]
            self._days.append(Day(day_data=day_data))
    
    def getWeekMeals(self):
        return [day.getTodaysMeals() for day in self._days]
        
    def getTodaysMeal(self): #Returns todays or next mondays Meal (If Weekday is Saturday or Sunday)
        return self._days[self.__today()].getTodaysMeals()
        
    def __today(self):
        today = datetime.datetime.weekday(datetime.datetime.today())
        if today > 4:
            return 0
        return today
