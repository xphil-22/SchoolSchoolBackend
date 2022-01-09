from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from canteen.scripts import Canteen

# Create your views here.
class getWeekMeals(APIView): #View to get the Meals of the Week
    authentication_classes = [TokenAuthentication, SessionAuthentication] #Authentification allowed with Session or Token Auth
    permission_classes = [IsAuthenticated] #Acces allowed when User is Authenticated (Logged in)
    
    def get(self, request, format=None):    #Get Request
        MensaInstitutsviertel = Canteen.Canteen() #Canteen Object created 
        MealsThisWeek = MensaInstitutsviertel.getWeekMeals() #Call getWeekMeals Method of Canteen Class
        return JsonResponse({"Meals" : MealsThisWeek}) #Return as Json Object

class getDayMeal(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication] #Authentification allowed with Session or Token Auth
    permission_classes = [IsAuthenticated] #Acces allowed when User is Authenticated (Logged in)
    
    def get(self, request, format=None): #Get Request
        MensaInstitutsviertel = Canteen.Canteen() #Canteen Object created 
        MealToday = MensaInstitutsviertel.getTodaysMeal() #Call getTodaysMeals Method of Canteen Class
        return JsonResponse({"Meals" : MealToday}) #Return as Json Object