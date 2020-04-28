from pprint import pprint as pp
from bs4 import BeautifulSoup
import phonenumbers
import json

class Data(object):
    pass

def getPhoneNumber(aString):
    #Delaware has two numbers, would fail the test
    if "302-998-7161, 302-444-4761" in aString:
        return aString
    try:
       theNumber = phonenumbers.parse(aString, "US")
       if not phonenumbers.is_valid_number(theNumber):
           return None
       return theNumber
    except:    
       return None


from pathlib import Path
def createObjects(dataClass):
    path = Path(__file__)
    directory = path.parent.joinpath('data')

    f = open (directory,'r')
    data = f.read()
    f.close()
    soup = BeautifulSoup(data, 'html.parser')
    items = soup.find_all('p')
    allData  = []
    allDicts = []
    for party in items:
        pp (party)
            
        data = dataClass()
        allDicts.append(data.__dict__)
        allData.append(data) 
        strong = party.strong
        data.title = strong.text
        strong.extract()
        links = party.find_all('a')
        for link in links:
                link.extract()
                href= link.get('href').lower()
                text = link.text
                if 'instagram' in href:
                    data.instagramId = href.split("instagram")[1]
                elif 'twitter' in href:
                    data.twitterId = href.split("twitter.com/")[1]
                elif 'Facebook Group' in text:
                      groupId = href.split("/")
                      data.facebookGroup = groupId[4]
                elif 'Facebook Link' in text:
                      data.facebookId = href.split("/")[3]             
                else:
                   data.url = href
            
        address = str(party)
        address=address = address.replace( '\xa0','')
        address=address = address.replace( '<p>','')
        address=address = address.replace( '</p>','')
        address=address = address.replace( '\n','')    
        address=address = address.replace( '|','')
        address=address.replace('<span>','')
        address=address.replace('</span>','')
        address=address.replace('<em>','')
        address=address.replace('</em>','')
        address=address.replace('<strong>','')
        address=address.replace('</strong>','')        
        address = address[5:]
        result = ''
        previous = ''
        for item in address:
            if item == ' ' and previous == ' ':
               continue
            previous = item
            result += item
        address = result.split('<br/>')
        result = []
        for item in address:
            if item in ['',' ']:
               continue
            phone = getPhoneNumber(item)
            if phone == None:
                result.append(item)
            else:
                data.phone = phone        
        data.address = ' \n '.join(result)
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

    
