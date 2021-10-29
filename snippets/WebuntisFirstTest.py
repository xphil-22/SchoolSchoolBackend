import webuntis
import datetime
import json


s = webuntis.Session(
    server='https://terpsichore.webuntis.com',
    username='philipp.wissler',
    password='Siss2021!',  
    school='RFGS-Freiburg', 
    useragent='WebUntis Test'
    ).login()


klassenID = s.klassen().filter(name='TGI12/4')[0].id

today = datetime.date.today()
monday = today - datetime.timedelta(days=today.weekday())
friday = monday + datetime.timedelta(days=4)

TodayOrNextSchoolDay = datetime.date.today()

if today.weekday() >= 5:
    TodayOrNextSchoolDay = today - datetime.timedelta(days=today.weekday()) + datetime.timedelta(days=7) #Calculate Monday and add one Week to get the next Monday


print(TodayOrNextSchoolDay)

klasse = s.klassen().filter(id=klassenID)[0]  
#NextWeek = datetime.date(2021, , 01)
#print(NextWeek)
#tt = s.timetable(klasse=klasse, start=NextWeek, end=NextWeek)

#print(tt)

"""
a = s.klassen()
print(a)
"""