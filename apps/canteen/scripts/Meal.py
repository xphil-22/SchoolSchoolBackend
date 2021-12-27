import requests
from lxml import etree
from bs4 import BeautifulSoup
from datetime import datetime

class Meal:
    def __init__(self, name:str=None, main_dish:str=None, cost_students:str=None, cost_teachers:str=None, cost_visitors:str=None, allergents:str=None, *remaining_info):
        
        self._name = name
        self._main_dish = main_dish
        self._cost_students = cost_students
        self._cost_teachers = cost_teachers
        self._cost_visitors = cost_visitors
        self._allergents = allergents
        self._remaining_info = remaining_info

    def getMealDetails(self):
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
    
    def __str__(self) -> str:
        temp = '\n '.join([i for i in self.remaining_info]) # have to do this, '\' is not possible in {expression} part of f-strings
        return f"{self.name}\n {self.main_dish}\n {temp}\n {self.allergents}\n {self.cost_students}"