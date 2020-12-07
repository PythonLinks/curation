from zope.interface import implementer

from zopache.core.relatives import Parents
from zopache.business.ipolitician import IPolitician
from zopache.business.interfaces import IOrganization
from zopache.business.ipolitician import IPolitician
from zopache.pages.location import LocationContainer
from zopache.business.interfaces import IRegion

class RegionBase(LocationContainer):

    
    def parentsWhichImplement(self,interface):
           item = self
           result=[]
           while (item!=None):
             if interface.providedBy(item):
                       result.append(item)
             item=item.__parent__
           return result

    def getMapPoliticians (self):

        if self.isNationalMap():
           return self.searchAllPoliticians(
                  candidates = True,
                  electedOfficials = True,
                  partyOfficers = True,
                  isGreen = True
                 )
        else:
           return self.searchBranchPoliticians(
                  candidates = True,
                  electedOfficials = True,
                  partyOfficers = True
                 )            

                      
    def getListPoliticians(self):
        if self.isNationalMap():
           return self.searchAllPoliticians(
                  candidates = True,
                  electedOfficials = True,
                  partyOfficers = True,
                  isGreen = True,
                  isNational = True
                 )
        else:
           return self.searchBranchPoliticians(
                  candidates = True,
                  electedOfficials = True,
                  partyOfficers = True,
                 )
    
    def isNationalMap (self):        
        return self.parentLength() == 1

    def parentLength(self):        
        parents = self.parentsWhichImplement(IOrganization)
        parentLength = len(parents)
        return parentLength    

    def searchAllPoliticians(self,
                             all = False, 
                             candidates = False,
                             electedOfficials = False,
                             partyOfficers = False,
                             isGreen = False,
                             isNational = False
                             ):
    
            siteRoot = self.getSiteRoot()
            allPoliticians = siteRoot.politicians.values()
            return self.actuallySearch(                       
                       allPoliticians,
                       all,
                       candidates,
                       electedOfficials,
                       partyOfficers,
                       isGreen,
                       isNational)
        
    def searchBranchPoliticians(self,
                             all = False, 
                             candidates = False,
                             electedOfficials = False,
                             partyOfficers = False,
                             isGreen = False,
                             isNational = False
    ):
        politicians = [] 
        parents = self.parentsWhichImplement(IOrganization)
        parentLength = len(parents)
        
        #THE STATE PAGES
        if parentLength == 2:
            children = []
            children = self.getCompaniesRecursively(children)
            for item in children:
                if IPolitician.providedBy(item):
                         if item.isCandidate() or item.isElectedOfficial():
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
        
    def actuallySearch(self,
                       aList,
                       all,
                       candidates,
                       electedOfficials,
                       partyOfficers,
                       isGreen,
                       isNational):
        result = []
        for person in aList:
            if all:
                result = self.maybeAppend(person, result, isGreen, isNational)
            elif candidates and person.isCandidate():
                result = self.maybeAppend(person, result, isGreen, isNational)
            elif electedOfficials and person.isElectedOfficial():
                result = self.maybeAppend(person, result, isGreen, isNational)
            elif partyOfficers and person.isPartyOfficer():
                result = self.maybeAppend(person, result, isGreen, isNational)
        return result
        
    def maybeAppend(self,person, result, isGreen, isNational):
           if not isGreen or person.isGreen():
               if not isNational or person.isNational():
                  result.append(person)       
           return  result

        #FOR STATE AND LOCAL MAPS FIRST GET THE TWO NATIONAL
        #POLITICIANS IN THE NATIONAL MAP.  HOWIE AND ANGELA
        #byClass = list(map(lambda x: x.sortByClass(), parents))
        #politicians = byClass[0]['Politician']


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
        
    
@implementer(IRegion)
class Region(RegionBase):

    def hasFutureEvent(self):
        return False
