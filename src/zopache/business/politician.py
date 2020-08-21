from zope.interface import implementer

from zopache.business.company import GeoBase
from zopache.pages.location import LocationLeaf
from zopache.business.ipolitician import (IPolitician,
                                          IAddPolitician,
                                          IPoliticiansSite)
from zopache.pages.page import SiteRoot
from zopache.business.region import Region


@implementer (IPolitician)
class Politician (GeoBase,LocationLeaf):
    localOrNational = ""
    webClass = "Politician"
    clientClass = "category"
   

    def proxyValues(self):
       real = list(self.values())
       webClass = getWebClass  **
       imaginary = self.proxyChildren(webClass)
       return real + imaginary
       
    def proxyChildren(self,origin):
       result = []
       For item in origin():
           if ITemplate.providedBy (item):
           result.append(Imaginary(self,item)):
       return result                


    #I THINK THIS IS NEVER USED. 
    def get(self,name,default = None):
       result = super().get(name,default)
       if result:
          return result
       
       siteRoot = self.getSiteRoot()
       templateRoot = siteRoot[siteRoot.templateRoot]
       slugs = name.split(".")
       if name in templateRoot:
          item = templateRoot [name]
          if IBTreeContainer.providedBy(item):              
             return ImaginaryBTree(name,item)
          else:
             return Imaginary(name,item)              
       return default

@implementer (IPoliticiansSite)
class PoliticiansSite (GeoBase,LocationLeaf,SiteRoot):
    webClass = "Politician"
    clientClass = "category"    
    def __init__(self):
        SiteRoot.__init__(self)
        GeoBase.__init__(self)
        LocationLeaf.__init__(self)

