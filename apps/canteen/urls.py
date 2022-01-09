from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from canteen import views
#Urls that are linking to the specific Class-Based-View or Function-Based-View

urlpatterns = [ #Interface to link to the right View
    path('getWeekMeals/', views.getWeekMeals.as_view()),
    path('getDayMeal/', views.getDayMeal.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
