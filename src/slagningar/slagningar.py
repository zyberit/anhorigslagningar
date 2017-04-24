'''
Created on 23 apr. 2017

@author: hakan
'''

import io, csv
from .models import Case, Slagningar
from datetime import datetime

def loadfile(f):
#     Slagningar.objects.all().delete()
#     Case.objects.all().delete()
    
    x = io.StringIO(f.read().decode("utf-8"))
#     a = [{k: v for k, v in row.items()} for row in csv.DictReader(x, skipinitialspace=True)]

    newcases = None
    reader = csv.DictReader(x)
    for row in reader:
        if newcases == None:
            newcases = Case()
            newcases.save()
        slagning = Slagningar()
        slagning.timestamp = datetime.strptime(row["Tidpunkt event"], "%b %d %Y %H:%M:%S")  #Mar 07 2017 15:40:23
        slagning.system = row["SystemId"]
        slagning.signatur = row["AnvändarID"]
        slagning.action = row["Händelsetyp"]
        slagning.objekt = row["ObjektId"]
        slagning.relation = row["Relation"]
        slagning.info1 = row["Objektinfo"]
        slagning.info2 = row["Reserv 1"]
        slagning.info3 = row["Reserv 2"]
        slagning.workplace = row["Anstalldes arbetsort"]
        slagning.office = row["Anstalldes Af-kontor"]
        slagning.boss = row["Anstalldes narmsta chef"]
        slagning.mo = row["Anstalldes MO"]
        slagning.moboss = row["Anstalldes Mo/Avd -chef"]
        slagning.case = newcases
        slagning.save()

    if newcases != None:
        newones = Slagningar.objects.filter(case=newcases).order_by('signatur','timestamp')
        acase = None
        for n in newones:
            if acase == None or (acase.signatur != n.signatur and acase.objekt != n.objekt):
                acase = Case()
                acase.date = n.timestamp.date()
                acase.signatur = n.signatur
                acase.objekt = n.objekt
                acase.boss = n.boss
                acase.action = -1
                acase.save()
            n.case = acase
            n.save()
        newcases.delete()
            



def loadfileX(f):
#     Slagningar.objects.all().delete()
#     Case.objects.all().delete()
    
    x = io.StringIO(f.read().decode("utf-8"))
#     a = [{k: v for k, v in row.items()}
#          for row in csv.DictReader(x, skipinitialspace=True)]
    newcase = Case()
    newcase.signatur = "NEW!!"
    newcase.save()

    reader = csv.DictReader(x)
    for row in reader:
        slagning = Slagningar()
        slagning.timestamp = datetime.strptime(row["Tidpunkt"], "%b %d %Y %H:%M:%S")  #Mar 07 2017 15:40:23
        slagning.system = row["System"]
        slagning.signatur = row["Signatur"]
        slagning.objekt = row["Objekt"]
        slagning.relation = row["Relation"]
        slagning.info1 = row["Info 1"]
        slagning.info2 = row["Info 2"]
        slagning.info3 = row["Info 3"]
        slagning.workplace = row["AnstÃ¤lldes arbetsort"]
        slagning.office = row["Af-kontor"]
        slagning.boss = row["NÃ¤rmsta chef"]
        slagning.mo = row["AnstÃ¤lldes MO/Avd"]
        slagning.moboss = row["MO/Avd-chef"]
        slagning.case = newcase
        slagning.save()
    
    newones = Slagningar.objects.filter(case=newcase).order_by('signatur','timestamp')
    newcase = None
    for n in newones:
        if newcase == None or (newcase.signatur != n.signatur and newcase.objekt != n.objekt):
            newcase = Case()
            newcase.date = n.timestamp.date()
            newcase.signatur = n.signatur
            newcase.objekt = n.objekt
            newcase.boss = n.boss
            newcase.action = -1
            newcase.save()
        n.case = newcase
        n.save()
            
    
    
    
    
    