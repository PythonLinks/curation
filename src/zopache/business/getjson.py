from slugify import slugify
import json
import os

here =  os.path.dirname(os.path.abspath(__file__))
source = os.path.join(here,"usdata.json")
source = open(source)
inner = json.load(source)
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



