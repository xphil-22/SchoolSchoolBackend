from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from untis import views


urlpatterns = [
    path('webuntis/login/', views.WebUntisLogin.as_view()),
    path('webuntis/changePassword/', views.changePassword.as_view()), 
    path('webuntis/',views.webuntis),
]

urlpatterns = format_suffix_patterns(urlpatterns)
