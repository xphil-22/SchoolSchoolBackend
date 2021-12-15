import requests
from lxml import etree
from bs4 import BeautifulSoup
from datetime import datetime


url = "https://www.swfr.de/essen-trinken/speiseplaene/mensa-institutsviertel/"
day_acronyms = ["mon", "tue", "wed", "thu", "fri"]

class Meal:
    def __init__(self, name:str, main_dish:str, cost_students:str, cost_teachers:str, cost_visitors:str, allergents:str, *remaining_info):
        self.name = name
        self.main_dish = main_dish
        self.cost_students = cost_students
        self.cost_teachers = cost_teachers
        self.cost_visitors = cost_visitors
        self.allergents = allergents
        self.remaining_info = remaining_info

    def getMealDetails(self):
        return[
            {"name":self.name},
            {"main_dish":self.main_dish},
            {"cost_students":self.cost_students},
            {"cost_students":self.cost_students},
            {"cost_teachers":self.cost_teachers},
            {"cost_visitors":self.cost_visitors},
            {"allergents":self.allergents},
            {"remaining_info":self.remaining_info},
        ]
    
    def __str__(self) -> str:
        temp = '\n '.join([i for i in self.remaining_info]) # have to do this, '\' is not possible in {expression} part of f-strings
        return f"{self.name}\n {self.main_dish}\n {temp}\n {self.allergents}\n {self.cost_students}"

class Day:
    def __init__(self, date:str, meals:list[Meal]) -> None:
        self.date = date
        self.meals = meals
    
    def getMealOfDay(self):
        return {"meals": 
                    [
                        {"date":self.date},
                        {"meals" : [m.getMealDetails() for m in self.meals]}
                    ]
                }
    
def getMeals():
    r = requests.get(url)

    soup = BeautifulSoup(r.text, features="lxml")
    html = etree.HTML(str(soup))

    days = []

    def get_day(day_acronym):
        day_data = html.xpath(f"//*[@id=\"tab-{day_acronym}\"]")[0]

        date = ""
        meals = []

        for element in day_data:
            if element.tag == "h3":
                date = element.text
            else:
                data = list(element.itertext())
                meal = Meal(data[0], data[1].lstrip(), data[-5], data[-3], data[-1], data[-7], *data[2:-7])
                meals.append(meal)
        return date, meals[0:-1] # [0:-1] filters out Buffets, because they are still broken

    for day_acronym in day_acronyms: # loop through each day, to get only one day just use get_day("mon") for monday
        days.append(Day(*get_day(day_acronym)))


    def getNextMealWeekday():
        today = datetime.today().weekday()
        if today > 4:
            return 0
        return today

    return days[getNextMealWeekday()].getMealOfDay()