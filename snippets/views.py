from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from snippets.permissions import IsCreator, IsAdminOrCreator, SnippetListPermission
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.http import HttpResponseRedirect
from rest_auth.views import LoginView
from django.core.exceptions import SuspiciousOperation
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from snippets import untis
import webuntis
# Create your views here.


class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [SnippetListPermission] #Normal User is allowed to do a POST #Admin can do anything
    
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


    def post(self, request, format=None):
        if not self.request.user.profile.snippetID:
            serializer = SnippetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=self.request.user)
                self.request.user.profile.snippetID = serializer.data['id']
                self.request.user.save() 
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response("invalid request, snippet already exists at snippets/{}".format(self.request.user.profile.snippetID), status=status.HTTP_403_FORBIDDEN)

    @csrf_exempt
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    #mixins.DestroyModelMixin,
                    generics.GenericAPIView):
                    
    
    #Normal User should be allowed to see and change the snippet when he is the creator
                                         
    permission_classes = [IsAdminOrCreator]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)



class UserList(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomLoginView(LoginView):
    def get_response(self):
        orginal_response = super().get_response()
        mydata = {"SnippetID": self.request.user.profile.snippetID}
        orginal_response.data.update(mydata)
        return orginal_response


"""
class WebUntis(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request, format=None):
        return Response()

    def post(self, request, format=None):
        #Raw_Data = request.data
        #untisUsername = Raw_Data['username']
        #untisPassword = Raw_Data['password']
        self.request.user.profile.untisUsername = "123456"
        self.request.user.save() 

        return Response(self.request.user.profile.untisUsername)
"""

class WebUntisRegistration(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated] 

    def post(self, request, format=None):
        Raw_Data = request.data
        if (Raw_Data['username'] and Raw_Data['password']) != None:
            u = untis.Untis()
            if u.newSession(Raw_Data['username'], Raw_Data['password']):  
                self.request.user.profile.untisUsername = Raw_Data['username'] 
                self.request.user.profile.untisPassword = Raw_Data['password']
                self.request.user.save()               
                return Response(status=status.HTTP_200_OK)
            else:
                 raise APIException("Wrong credentials")
           
           
           
           # server/WebUntis/registration #Body -> {"username":"value", "password":"value"}