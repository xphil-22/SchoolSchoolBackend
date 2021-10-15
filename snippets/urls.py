from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from snippets import views
from snippets.views import CustomLoginView
from django.urls import path, include

urlpatterns = [
    
    path('snippets/', views.SnippetList.as_view()),
    path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('custom/login/', CustomLoginView.as_view(), name='my_custom_login'),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)