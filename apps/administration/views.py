from rest_framework import generics
from django.contrib.auth.models import User
from administration.serializers import UserSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import SessionAuthentication
from rest_auth.views import LoginView

# Create your views here.

class UserList(generics.ListAPIView):   #List all Users (Only visible for Admins)
    permission_classes = [IsAdminUser]  
    authentication_classes = [SessionAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView): #List Details about a User. For Example Mail Adress (Only visible for Admins)
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CustomLoginView(LoginView):   #Login View that saves the SnippetID in the UserDataTable of the Database (Override of the LoginView)
    def get_response(self):         
        orginal_response = super().get_response()
        mydata = {"SnippetID": self.request.user.profile.snippetID}
        orginal_response.data.update(mydata)
        return orginal_response