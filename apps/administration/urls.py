from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from administration import views
from django.contrib import admin
#Urls that are linking to the specific Class-Based-View or Function-Based-View

urlpatterns = [ #Interface to link to the right View
    path('admin/', admin.site.urls),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    path('login/', views.CustomLoginView.as_view(), name='my_custom_login'),
    path('registration/', include('rest_auth.registration.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
