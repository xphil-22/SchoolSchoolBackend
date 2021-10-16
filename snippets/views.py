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



    #@csrf_exempt
    """
    def post(self, request, *args, **kwargs):
        if self.request.user.profile.snippetID:
            newSnippet = self.create(request, *args, **kwargs)
            #self.request.user.profile.snippetID = self.request.user.id #Change to actualSnippetId
            #self.request.user.save() 

            #return newSnippet
            x = None
            if SnippetSerializer.is_valid(self):
                x = SnippetSerializer.save(self, owner=self.request.user)
            raise SuspiciousOperation("Code :  {}".format())
            #return Response(request.user.profile.snippetID)#
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
            
        #raise SuspiciousOperation("invalid request, snippet already exist at: {}".format(self.request.user.profile.snippetID))

        #Extract id of the object using reverse()
        #Edit user.SnippetID = id
        """
        
    #def create(self, request, *args, **kwargs):
        #response = super(SnippetList, self).create(request, *args, **kwargs)
        # here may be placed additional operations for
        # extracting id of the object and using reverse()
        #red_url = "http://localhost:8000/snippets"+request
        #return HttpResponseRedirect(redirect_to=red_url)
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

    #def delete(self, request, *args, **kwargs):
    #    return self.destroy(request, *args, **kwargs)


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