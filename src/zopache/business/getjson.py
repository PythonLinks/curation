from slugify import slugify
import json
from zopache.business.usdata import  inner


states = {}

for item in inner:
    stateName = item['properties']['name']
    stateName = slugify (stateName)
    states[stateName] = item

def getStateJson(state):    
   stateName = state.name
   return getJson(stateName)

def getJson(stateName):
   outer = {"type":"FeatureCollection","features":[]}
   outer['features'].append(states[stateName])
   outer = json.dumps(outer)
   return outer



