from django.views.decorators.csrf import csrf_exempt
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from rest_framework import status, mixins, generics
from rest_framework.response import Response
from SchoolSchoolBackend.permissions import IsAdminOrCreator, SnippetListPermission
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

# Create your views here.


class SnippetList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [SnippetListPermission] #Normal User is allowed to do a POST, Admin can do anything (including get)
                                                 #SnippetListPermission is written in 'SchoolSchoolBackend/permissions' file
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

class SnippetDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    #Normal User should is allowed to see and change the snippet if he is the creator
                                         
    permission_classes = [IsAdminOrCreator]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


    
    
 