from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from untis import views

#Urls that are linking to the specific Class-Based-View or Function-Based-View

urlpatterns = [ #Interface to link to the right View
    path('webuntis/login/', views.WebUntisLogin.as_view()),
    path('webuntis/changePassword/', views.changePassword.as_view()), 
    path('webuntis/',views.webuntis),
]

urlpatterns = format_suffix_patterns(urlpatterns)
