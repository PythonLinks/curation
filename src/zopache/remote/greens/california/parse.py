from pprint import pprint as pp
from bs4 import BeautifulSoup
import phonenumbers
import json
from pathlib import Path

class Data(object):
    pass


def createObjects(dataClass):
    path = Path(__file__)
    directory = path.parent.joinpath('data')
    f = open (directory,'r')
    data = f.read()
    f.close()
    soup = BeautifulSoup(data, 'html.parser')
    items = soup.find_all('p')
    mydivs = soup.findAll("div", {"class": "views-row"})
    allData  = []
    allDicts = []
    for theItem in items:
        breakpoint()        
        image = theItem.img
        website = theItem.findAll("div", {"class": "views-field-website"})
        title = theItem.findAll("div", {"class": "views-field-title"})
        title = title.extract()
        phone = theItem.findAll("div", {"class": "views-field-phone"})        
        email = theItem.findAll("div", {"class": "views-field-email"})        
        data = Data()
        allDicts.append(data.__dict__)
        allData.append(data) 
        data.title = strong.text
        links = party.find_all('a')
    return allDicts, allData


from slugify import slugify
def createOrganizations(context):
    from zopache.business.company import Organization
    allDicts, allData = createObjects(Organization)
    for party in allData:
       title = party.title
       slug = slugify (title)
       
       context [slug] = party
       party.__parent__ = context
    print("Data is loaded")    
       

def getAllDicts(dataClass):
    allDicts, allData = createObjects(dataClass)
    return allDicts    

if __name__ == "__main__":    
    allDicts = getAllDicts(Data)
    pp (allDicts)

    
