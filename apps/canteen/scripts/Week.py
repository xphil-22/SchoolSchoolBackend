from canteen.scripts.Day import Day
import datetime

class Week:
    def __init__(self, html) -> None:
        self._days = [] #List with days
        self._day_acronyms = ['mon','tue','wed','thu','fri'] #day acronyms
        
        for day_acronym in self._day_acronyms:
            day_data = html.xpath(f"//*[@id=\"tab-{day_acronym}\"]")[0]
            self._days.append(Day(day_data=day_data)) #Create Day with html data of current day_acronym and save this Day in days list
    
    def getWeekMeals(self): #call getTodaysMeals on every day and return each value saved in a list
        return [day.getTodaysMeals() for day in self._days]
        
    def getTodaysMeal(self): #Returns todays or next mondays Meal (If Weekday is Saturday or Sunday)
        return self._days[self.__today()].getTodaysMeals() #call getTodaysMeal on day that is calculated by __today method
        
    def __today(self) -> int: #Returns current day as int
        today = datetime.datetime.weekday(datetime.datetime.today())
        if today > 4:
            return 0
        return today
