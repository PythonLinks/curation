from urllib.request import urlopen
import json
import pickle
from bs4 import BeautifulSoup
from slugify import slugify
from zopache.climate.map import StrikeMap
from zopache.pages.location import Map
from zopache.pages.location import Location
from zopache.climate.strike import ClimateStrike
site = 'https://www.fridaysforfuture.org/events/map'
import transaction

def processData(countries,result):    
    strikeNumber =-1
    for strike in result:
      strikeNumber += 1
      countryName = strike["country"]
      countrySlugName = slugify(countryName)      
      if countrySlugName == "":
          continue
      if not countrySlugName in countries:
          country = StrikeMap()
          country.title = countryName
          country.strikes = []
          countries [countrySlugName]=country
                              
      #ADD THE STRIKE TO THE LIST OF STRIKES IN THAT COUNTRY
      country = countries [countrySlugName]
      newStrike = ClimateStrike()
      name = str(strikeNumber)
      print (strikeNumber)
      country[name] = newStrike
      newStrike.__name__ = name
      for key, value in strike.items():
               if key == "lon":
                   key = "longitude"
                   value = float(value)
               if key == "lat":
                   key = "lattitude"
                   value = float(value)                   
               setattr(newStrike,key,value)
      #THE STRIKE PARENT IS THE COUNTRY, SO DELETE THAT VARIABLE.
      del strike["country"]
      if not (len(newStrike.town) ==0) :
          newStrike.title = newStrike.town
      else:
          newStrike.title = newStrike.location
     
def getMapCenter(countries):
   for country in countries.values():
     print (country.__name__)  
     lat = 0.
     lon = 0.
     strikes = country.valuesAsList()     
     length = 0
     for strike in strikes:
           if not (hasattr(strike,'lattitude') and
                    hasattr(strike,'longitude')):
              continue
           try:
              lat += strike.lattitude
              lon += strike.longitude
              print (strike.lattitude,strike.longitude)
              length += 1
           except:
               import pdb; pdb.set_trace()
               pass
     country.longitude = lon / length
     country.lattitude =lat / length
     print (country.lattitude, country.longitude)
     print ("----------")
     print ()
     print ()
def doit(context):
  countries = Map()
  countries.title = "Global Maps of Climate STrikes"
  countries.description ="Please click into the country, and then into the city."
  countries.zoomLevel = 1.4
  countries.lattitude = 0.0
  countries.longitude = 0.0
  context ['global-climate-strike-map'] = countries



  with urlopen(site) as response:
    page = response.read()
    soup = BeautifulSoup(page, "html.parser")
    scripts = soup.find_all("script")
    result = scripts [4].text
    start = result.find ("=")
    result = result [start+1:-3]
    result = json.loads(result)
    
    processData (countries, result)
    getMapCenter(countries)






