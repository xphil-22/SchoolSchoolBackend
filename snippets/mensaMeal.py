import requests
from lxml import etree
from bs4 import BeautifulSoup


# making a meal class in order to save the meal information

class Meal:
    def __init__(self, name:str, main_dish:str, supplement:str, garnish:str, cost_students:str, cost_teachers:str, cost_visitors:str):
        self.name = name
        self.main_dish = main_dish
        self.supplement = supplement
        self.garnish = garnish
        self.cost_students = cost_students
        self.cost_teachers = cost_teachers
        self.cost_visitors = cost_visitors
    
    def getMeal(self):
        return  [
                    {"name":self.name},
                    {"main_dish":self.main_dish},
                    {"supplement":self.supplement},
                    {"garnish":self.garnish},
                    {"cost_students":self.cost_students},
                    {"cost_teachers":self.cost_teachers},
                    {"cost_visitors":self.cost_visitors},
                ]
    
    def __str__(self) -> str:
        return f"{self.name}\n {self.main_dish}\n {self.supplement}\n {self.garnish}\n kostet: {self.cost_students}"


def getMeals():
    # define the url and the xpath for the right div to get the data from
    url = "https://www.swfr.de/essen-trinken/speiseplaene/mensa-institutsviertel/"
    xpath = "/html/body/div[2]/div/div[1]/div[6]/div[1]/div[3]/div[2]"

    # making the request and parsing it to a dom
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="lxml")
    dom = etree.HTML(str(soup))


    # using xpath to get to the right part of the dom
    dom_at_xpath = dom.xpath(xpath)[0]

    # traversing the dom to collect the data and saving it in an array of meals
    meals = []

    for part in dom_at_xpath:
        if part.tag == "div":
            iter_tags = ["div", "tr", "table"]
            tail_tags = ["br"]
            text_tags = ["span", "h4", "td"]
            data = []

            def p(part_of_dom):
                for element in part_of_dom:
                    if element.tag in iter_tags:
                        p(element)
                    elif element.tag in tail_tags:
                        data.append(element.tail)
                    elif element.tag in text_tags:
                        data.append(element.text)

            p(part)
            meals.append(Meal(data[0], data[1], data[2], data[3], data[8], data[10], data[12]))
            
    jsonMeals = []
    for meal in meals:
        jsonMeals.append(meal.getMeal())

    return {"meals":jsonMeals}