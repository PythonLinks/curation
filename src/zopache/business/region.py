from zope.interface import implementer

from zopache.core.relatives import Parents
from zopache.business.ipolitician import IPolitician
from zopache.business.interfaces import IOrganization
from zopache.business.ipolitician import IPolitician
from zopache.pages.location import LocationContainer
from zopache.business.interfaces import IRegion

@implementer(IRegion)
class Region(LocationContainer):
    def parentsWhichImplement(self,interface):
           item = self
           result=[]
           while (item!=None):
             if interface.providedBy(item):
                       result.append(item)
             item=item.__parent__
           return result

    def getMapPoliticians (self):
        return self.getPoliticians(True)        
               
    def getListPoliticians(self):
        return self.getPoliticians(False)

    def hasFutureEvent(self):
        return False
    
    def isGreen(self,item):
        if hasattr(item,'affiliation'):
            if item.affiliation == 'Independent':
                return False
            if item.affiliation == 'Democrat':
                return False
        return True
    
    def getPoliticians (self,isMap):        
        parents = self.parentsWhichImplement(IOrganization)
        parents.reverse()
        parentLength = len(parents)
        
        #THE NATIONAL PAGE
        if parentLength == 1:
            siteRoot = self.getSiteRoot()
            allPoliticians = siteRoot.politicians.values()
            if isMap:
               return list(allPoliticians)            
            nationalPoliticians = []
            for item in allPoliticians:
                  if  'National' in item.localOrNational:
                      if self.isGreen(item):
                         nationalPoliticians.append(item)
            return nationalPoliticians 

        #FOR STATE AND LOCAL MAPS FIRST GET THE TWO NATIONAL
        #POLITICIANS IN THE NATIONAL MAP.  HOWIE AND ANGELA
        byClass = list(map(lambda x: x.sortByClass(), parents))
        politicians = byClass[0]['Politician']
        #THE STATE PAGES
        if parentLength == 2:
            children = []
            children = self.getCompaniesRecursively(children)
            for item in children:
                if IPolitician.providedBy(item):
                      if self.isGreen(item):                    
                         politicians.append(item)
            return politicians
        
        #FOR LOCAL PAGES 
        if parentLength > 2:
            politicians = []
            for parent in parents:
                for item in parent.values():
                    if IPolitician.providedBy(item):
                        politicians.append(item)
            return politicians    

    def mapPoints(self):
        result = []

        politicians = self.getMapPoliticians()
        return politicians  +  self.getOrganizations()
    
    def getOrganizations(self):
        result = []
        showChildren = self.showChildren
        for item in self.values():
            if not IOrganization.providedBy(item):
                continue

            if not item.webApproved:
                continue

            if item.hasFutureEvent() :
                    result.append(item)

            if showChildren  :
                result.append(item)
            else:
                result = result + item.getOrganizations()
        return result
        
