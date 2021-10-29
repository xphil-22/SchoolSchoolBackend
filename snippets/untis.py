import webuntis
import datetime
import json

class Untis:
    def __init__(self):
        self._session = 0
    
    def newSession(self, username, password):
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
            print("False")
            return False
    