from canteen.scripts.Meal import Meal

class Day:
    def __init__(self, day_data):
        self._day = True
        self._meals =[]
        self._date = ""
        
        if list(day_data[1].itertext())[0] == 'heute keine Essensausgabe':
            self._date = list(day_data[0].itertext())[0]
            self._day = False
            
        else:
            for element in day_data:
                if element.tag == "h3":
                    self._date = element.text
                if element.tag == "h4":
                    print("xxxxxxxxxxxxxxxxxxxx", element.text)    
                
                else:
                    data = list(element.itertext())

                    meal = Meal(data[0], data[1].lstrip(), data[-5], data[-3], data[-1], data[-7], *data[2:-7])
                    self._meals.append(meal)
                
    def getTodaysMeals(self):
        if self._day:
            return self._date, [meal.getMealDetails() for meal in self._meals]
        return {"date":self._date}, {"meal":'heute keine Essensausgabe'}
       #return date, meals[0:-1] # [0:-1] filters out Buffets, because they are still broken
        

    