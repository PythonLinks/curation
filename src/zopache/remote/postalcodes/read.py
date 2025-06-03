import json
from pathlib import Path

from zopache.remote.postalcodes.postalcode import PostalCode

def createOneZipCode (data,directory):
    zipCode = str(data['zip_code'])
    length = len(zipCode)
    zipCode = '0'*(5-length) + zipCode
    print (zipCode)
    new = PostalCode(
                      zipCode,
                      data['latitude'], 
                      data['longitude'], 
                      data['county'],
                      data['city'],                       
                      data['state'])
    directory[new.__name__] = new
    new.__parent__ = directory
    
def createCodes(inDirectory):
    # Open and read the JSON file
    path = Path(__file__)
    path = path.parent / 'USZipCodes.json'
    with open(path , 'r') as file:
        zipCodes= json.load(file)
        for data in zipCodes:
            createOneZipCode(data, inDirectory)




