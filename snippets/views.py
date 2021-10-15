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



    #@csrf_exempt
    def post(self, request, *args, **kwargs):
        
        return self.create(request, *args, **kwargs)    
        #Extract id of the object using reverse()
        #Edit user.SnippetID = id
        #return the SnippetList Detail

    #def create(self, request, *args, **kwargs):
        #response = super(SnippetList, self).create(request, *args, **kwargs)
        # here may be placed additional operations for
        # extracting id of the object and using reverse()
        #red_url = "http://localhost:8000/snippets"+request
        #return HttpResponseRedirect(redirect_to=red_url)
    @csrf_exempt
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def update_profile(self, request, user_id):
        user = User.objects.get(pk=user_id)
        user.profile.SnippetID = 422
        user.save()

class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
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

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


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
        mydata = {"message": "some message", "status": "success"}
        orginal_response.data.update(mydata)
        return orginal_response