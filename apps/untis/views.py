from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from untis.scripts.Webuntis import WebsiteUntis
from untis.scripts.UntisAPI import UntisAPI

# Create your views here.

class WebUntisLogin(APIView): #Webuntis Login 
    # server/WebUntis/Login #Body -> {"username":"value", "password":"value"}
    authentication_classes = [TokenAuthentication, SessionAuthentication] #Authentification allowed with Session or Token Auth
    permission_classes = [IsAuthenticated]  #Acces allowed when User is Authenticated (Logged in)

    def post(self, request, format=None):
        Raw_Data = request.data #Given Parameters in the body
        if (Raw_Data['username'] and Raw_Data['password']) != None: #Check if there is password and username
            u = UntisAPI()
            if u.newSession(Raw_Data['username'], Raw_Data['password']):  #check if credentials are right
                self.request.user.profile.untisUsername = Raw_Data['username'] 
                self.request.user.profile.untisPassword = Raw_Data['password']
                self.request.user.save()               
                return Response({"LoginData":True})
            else:
                 raise APIException("Wrong credentials")
           
           
class changePassword(APIView): #change Password view same as Login View 
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated] 

    def post(self, request, format=None):
        Raw_Data = request.data
        if (Raw_Data['username'] and Raw_Data['password']) != None:
            u = UntisAPI()
            if u.newSession(Raw_Data['username'], Raw_Data['password']):  
                self.request.user.profile.untisUsername = Raw_Data['username'] 
                self.request.user.profile.untisPassword = Raw_Data['password']
                self.request.user.save()               
                return Response({"LoginData":True})
            else:
                 raise APIException("Wrong credentials")
             
@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes((TokenAuthentication, SessionAuthentication))
def webuntis(request): #webuntis view (function Based)
    
    try:
        username = request.user.profile.untisUsername #check if credentials are already saved in database
        password = request.user.profile.untisPassword
        
    except:
        return JsonResponse({"data":"You have to Login first" })
    
    if username == "" or password == "":
        return JsonResponse({"data":"You have to Login first"})
     
    if request.GET.get('subjects') == "": #when Parameter equals "subjects" try to download the subject of the saved user
        webuntis = WebsiteUntis(request.user.profile)
        if webuntis.Login():
            return JsonResponse(webuntis.getWebSubjects())
        else:
            return JsonResponse({"data": "Wrong Webuntis credentials in Database, maybe you have to change your Login Data via: 'webuntis/changeLoginData'"})   
    
    ### Old Functions ###
    if request.GET.get('classes') == 'all':
        u = UntisAPI()
        loggedIn = u.newSession(username, password)
        
        if loggedIn:
            klassen = u.getClasses()
            arr = []
            for klasse in klassen:
                arr.append(klasse.name)  
            return JsonResponse(arr, safe=False)
        else:
            return HttpResponse("Wrong Webuntis credentials in Database, maybe you have to change your Login Data via: 'webuntis/changeLoginData'")
     
    elif request.GET.get('ClassSubjectsOf'):
        u = UntisAPI()
        loggedIn = u.newSession(username, password)
        if loggedIn:
            subs = u.getSubjects(request.GET.get('ClassSubjectsOf'))
            return JsonResponse(subs, safe=False)
        else:
            return HttpResponse("Wrong Webuntis credentials in Database, maybe you have to change your Login Data via: 'webuntis/changeLoginData'")
    
    return HttpResponse("Wrong Keyword") 
