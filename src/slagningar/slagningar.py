'''
Created on 23 apr. 2017

@author: hakan
'''

import io, csv
from .models import Case, Slagningar
from datetime import datetime
import xml.etree.ElementTree as ET

def loadfile(f):
    Slagningar.objects.all().delete()
    Case.objects.all().delete()
    
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
            if acase == None or acase.signatur != n.signatur or acase.objekt != n.objekt or acase.date != n.timestamp.date():
                acase = Case()
                acase.date = n.timestamp.date()
                acase.signatur = n.signatur
                acase.objekt = n.objekt
                acase.boss = n.boss
                acase.action = -1
                acase.save()
#                 print (acase)
            n.case = acase
            n.save()
        newcases.delete()
            

def load_idmfile(xmlfile):
    ns3 = "{http://www.previa.se/schema/customer/base/v1}"
    
    ORGUNITS = {}
    USERS = {}
    MANAGERS = {}
    PNUM = {}
    
    root = ET.parse(xmlfile).getroot()
    
    # Find all organization units in list
    ous = root.find('Organization').find('OrganizationalUnits').findall('OrganizationalUnit')
    for ou in ous:
        UnitID = ou.find('UnitID').text
        Name = ou.find('Name').text.title()
        Active = ou.find('Active').text
        if Active == "true":
            # Create a new ORGUNIT with unit-number as index and add its name
    #        ORGUNITS[UnitID] = {'Name':Name, 'EmployeeCount':0}
            ORGUNITS[UnitID] = {'Name':Name}
    
    # Find all users in list
    users = root.find('Employments')
    for user in users:
        PersonKey = user.find('PersonKey').text # Personnummer
        Signatur = user.find('EmploymentNumber').text   # Signatur
        Email = user.find('Email').text
#         if user.find('PhoneNumber') != None:
#             PhoneNumber = user.find('PhoneNumber').find('NumberRelaxed').text
#         else:
#             PhoneNumber = "0771416416"
        PhoneNumber = MobileNumber = "0771416416"
        phones = user.findall('PhoneNumber')
        for phone in phones:
            if phone.find('Role').text == "Contact Number":
                PhoneNumber = phone.find('NumberRelaxed').text
            if phone.find('Role').text == "SMS Number":
                MobileNumber = phone.find('NumberRelaxed').text
        GivenName = user.find('GivenName').text
        Surname = user.find('Surname').text
        EmployedAt = user.find('EmployedAt').get(ns3+'unitRef')
        # Create a cross reference personnummer <-> signatur
        PNUM[PersonKey] = {'Signatur':Signatur}
        # Create a new user with signatur as key
        if EmployedAt in ORGUNITS.keys():
            orgname = ORGUNITS[EmployedAt]['Name']
        else:
            orgname = ""
        USERS[Signatur] = {'GivenName':GivenName, 'Surname':Surname, 'PhoneNumber':PhoneNumber, 'MobileNumber':MobileNumber, 'Email':Email, 'EmployedAt':orgname, 'EmployedAtUnit':EmployedAt}
    #    ORGUNITS[EmployedAt]['EmployeeCount'] += 1
    
    managers = root.find('Managers')
    for manager in managers:
        ManagerRef = manager.find('ManagerRef').find('PersonRef').text
#        MANAGERS[USERS[ManagerRef]['EmploymentNumber']] = USERS[ManagerRef]
        if USERS.has_key(PNUM[ManagerRef]['Signatur']):     # ???
            MANAGERS[PNUM[ManagerRef]['Signatur']] = USERS[PNUM[ManagerRef]['Signatur']]
            DependentEntityList = manager.find('DependentEntityList').findall('DependentEntity')
            for DependentEntity in DependentEntityList:
                if len (DependentEntity.findall('OrganizationalUnit')) != 0:
                    unitRef = DependentEntity.find('OrganizationalUnit').get(ns3+'unitRef')
                    if ORGUNITS.has_key(unitRef):
                        ORGUNITS[unitRef].update({'Manager':PNUM[ManagerRef]['Signatur']})
#                    MANAGERS[PNUM[ManagerRef]['Signatur']]['ManagerAt'] = ORGUNITS[unitRef]['Name']
    
    for org in ORGUNITS:
        if not ORGUNITS[org].has_key('Manager'):
            ORGUNITS[org]['Manager'] = "xxxxx"