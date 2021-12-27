from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from canteen.scripts import Canteen

# Create your views here.
class getWeekMeals(APIView): #TodaysMeal
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        MensaInstitutsviertel = Canteen.Canteen()
        MealsThisWeek = MensaInstitutsviertel.getWeekMeals()
        return JsonResponse({"Meals" : MealsThisWeek})

class getDayMeal(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        MensaInstitutsviertel = Canteen.Canteen()
        MealToday = MensaInstitutsviertel.getTodaysMeal()
        return JsonResponse({"Meals" : MealToday})