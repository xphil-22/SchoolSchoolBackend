import webuntis
import datetime
import json
import ast
import time


class UntisAPI:
    def __init__(self):
        self._session:webuntis.session = 0   #Session Object
        
    def newSession(self, username:str, password:str) -> bool: #Start a new Seesion and return if Session is valid (Credentials correct)
        try:
            s = webuntis.Session(
                server='https://terpsichore.webuntis.com',
                username= username,
                password= password,  
                school='RFGS-Freiburg', 
                useragent='WebUntis Test'
            ).login()
            self._session = s
            
            return True

        except:
            return False

    def getAllClasses(self) -> webuntis.objects.KlassenList: #return all classes of school 
        return self._session.klassen()
    
    def getSubjectsOfClass(self, className:str) -> webuntis.objects.SubjectList: #get all Subjects of the given class
        today = datetime.date.today()
        monday = today - datetime.timedelta(days=today.weekday())
        friday = monday + datetime.timedelta(days=6)
        klasse = self._session.klassen().filter(name=className)[0]  
        tt = self._session.timetable(klasse=klasse, start=monday, end=friday)
        
        ID_List = []
        for subject in tt:       
            s = str(subject)
            ID_List.append(int(s[s.find('su')+13:s.find(']', s.find('su'))-1]))

        ID_List = list(set(ID_List)) #To clear the array from duplicates
            
        subject_list = [str(subject) for subject in self._session.subjects()
                        if subject.id in ID_List]
        
        return subject_list
    
    
    