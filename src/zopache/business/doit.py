from urllib.request import urlopen
import json
from zopache.pages.location import Map
from zopache.pages.location import Location
from zopache.business.company import Company
site = 'https://maps.pythonlinks.info/json'

useClass = {
      "RegionGroup": Map,
      "LocationGroup" :Map,
      "CompanyGroup"  :Company,
      "CityGroup"     :Map
}

def processData(branch,root,context):
   for item in branch:
      itemClass = item["data"]["class"]
      if itemClass not in useClass:
             print (item["key"], itemClass)
             continue 
      new= useClass[itemClass]()
      newName = item["key"]
      if itemClass == "GroupCompany":
          newName = root.getUniqueNumberString()
      for key, value in item["data"].items():
               if key not in ["title","description","source",
                              "longitude","lattitude","zoom"]:
                              continue
               if key == "source":
                   try:
                      value = json.loads(value)
                   except:
                      value = " "
               if key == "zoom":
                   key = "zoomLevel"
               setattr(new,key,value)
      context[newName] = new
      root.addItem(new)

      if "children" in item:
          processData (item["children"],root,new) 
          
def doit(context):
  with urlopen(site) as response:
    page = response.read()
    tree = json.loads(page)
    root = tree [0]
    children = root["children"]
    pythonCompanies = children [2]
    processData ([pythonCompanies],context,context)






