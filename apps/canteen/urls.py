from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from canteen import views


urlpatterns = [
    path('getWeekMeals/', views.getWeekMeals.as_view()),
    path('getDayMeal/', views.getDayMeal.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
