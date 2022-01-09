import requests
from lxml import etree
from bs4 import BeautifulSoup
from datetime import datetime

class Meal:
    def __init__(self, name:str, main_dish:str, cost_students:str, cost_teachers:str, cost_visitors:str, allergents:str=None, *remaining_info:list):
        
        self._name:str = name
        self._main_dish:str = main_dish
        self._cost_students:str = cost_students
        self._cost_teachers:str = cost_teachers
        self._cost_visitors:str = cost_visitors
        self._allergents:str = allergents
        self._remaining_info:list[str] = remaining_info

    def getMealDetails(self) -> list[dict[str]]: #returns all meal attributes as dict in list
            return[
                {"name":self._name},
                {"main_dish":self._main_dish},
                {"cost_students":self._cost_students},
                {"cost_students":self._cost_students},
                {"cost_teachers":self._cost_teachers},
                {"cost_visitors":self._cost_visitors},
                {"allergents":self._allergents},
                {"remaining_info":self._remaining_info},
            ]
    
    def __str__(self) -> str: #Debbugging Method
        temp = '\n '.join([i for i in self.remaining_info]) # have to do this, '\' is not possible in {expression} part of f-strings
        return f"{self.name}\n {self.main_dish}\n {temp}\n {self.allergents}\n {self.cost_students}"