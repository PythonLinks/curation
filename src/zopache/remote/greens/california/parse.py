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
    for theItem in items:
        new = Data()
        new.imageURL = theItem.img
        new.remoteURL = theItem.findAll("div", {"class": "views-field-website"})
        title = theItem.findAll("div", {"class": "views-field-title"})
        new.title = title.extract()
        new.phone = theItem.findAll("div", {"class": "views-field-phone"})        
        new.email = theItem.findAll("div", {"class": "views-field-email"})             data.title = strong.text
        links = party.find_all('a')
        allData.append(new)
    return allData


from slugify import slugify
def createOrganizations(context):
    from zopache.business.company import Organization
    allData = createObjects(Organization)
    for party in allData:
       title = party.title
       slug = slugify (title)   
       context [slug] = party
       party.__parent__ = context
    print("Data is loaded")    
       

def getAllDicts(dataClass):
    allData = createObjects(dataClass)
    return allDicts    

if __name__ == "__main__":    
    allDicts = getAllDicts(Data)
    pp (allDicts)

    
