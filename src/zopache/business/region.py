from zope.interface import implementer

from zopache.core.relatives import Parents
from zopache.business.ipolitician import IPolitician
from zopache.business.interfaces import IOrganization
from zopache.business.ipolitician import IPolitician
from zopache.pages.location import LocationContainer
from zopache.business.interfaces import IRegion
from zopache.business.interfaces import IEvent

class RegionBase(LocationContainer):

    specialization = ''
    showChildren = True
   
    #JUST ADD ONE MARKER TO THE LIST                        
    def getOneMarker(self, firstItem, result):
                  if not hasattr(self, 'longitude'):
`                      return result,firstItem
                  if not firstItem:
                     result +=','
                  firstItem=False      
                  result+='\n'
                  result += '['
                  result +='"' +  self.__name__ + '"'
                  result += ','
                  result +='"' +  self.getTitle() + '"'
                  result += ','
                  lat,lng = self.getMarkerLatLng()
                  result +=  str(lat)  
                  result += ","                   
                  result += str(lng)
                  aClass = self.__class__.__name__[0]
                  result += self.getArg(aClass)
                  hasFutureEvent =  str(self.hasFutureEvent())
                  result += self.getArg(hasFutureEvent)
                  if self.__class__.__name__ in [
                          "Organization","MapOrganization"]:
                      focus = getattr(self,'focus',"")
                      focus = focus [:4]
                      result += ',"' + focus + '"'
                      
                  if self.__class__.__name__ == "Politician":
                     result += self.getArg(str(hasattr(
                                        self,'candidateInfo'))[0])
                     result += self.getArg(str(hasattr(
                                        self,'electedOfficial'))[0])
                     result += self.getArg(
                          str(hasattr(self,'partyOfficer'))[0])
                     result += self.getArg(
                          str(hasattr(self,'history'))[0])                     
                     outcome = self.getCandidateInfo("result")
                     if len(outcome) > 0:
                         outcome = outcome [0]
                     result += ',"' + outcome +' "'
                     
                  result += ',"' + self.remoteURL  + '"'                  
                  result += "]"
                  return result, firstItem
              
    def isElectedOfficial(self):
        if hasattr(self,'electedOfficial'):
           return True
        if self.getCandidateInfo("result") =="Won":
           return True
        return False                                   

    def getArg(self,aString,comma = True):
          result = ""
          if comma:
              result += ","
          result += '"'
          result += aString
          result += '"'
          return result
      
    def getColor(self):
        #COLOR BASED ON CLASS
        choose = {'Driver':'black',
                  'Business': 'yellow',
                  'Map': 'gold2x' 
                  }
        aClass = self.__class__.__name__
        if aClass in choose:
            return choose[aClass]

        #SELECT BASED On (CLASS, FUTURE EVENTS)
        hasFutureEvent = self.hasFutureEvent()
        choose = {
                  ('Politician',True):"orange",
                  ('Politician',False):"blue",
                  ('City',True):"orange",
                  ('City',False):"blue",            
                  ('MapOrganization',False):"red",                  
                  ('MapOrganization',True):"orange",                  
                  ('Organization',False):"red",
                  ('Organization',True):"orange",
                  ('Location',True):"bluered",
                  ('Location',False):"blue",
                  ('Company',True):"yellow2x",
                  ('Company',False):"yellow"                                    
                  }
        icon = choose[(aClass,bool(hasFutureEvent))]
        return icon
                        
    #ABOVE THIS FROM MAP
    
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
        return self.webClass == 'NationalMap'

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
        
        #THE STATE PAGES
        if self.webClass == 'SmallParty':
            children = []
            children = self.getCompaniesRecursively(children)
            for item in children:
                if IPolitician.providedBy(item):
                         if item.isCandidate() or item.isElectedOfficial():
                             politicians.append(item)
            return politicians
        
        #FOR LOCAL PAGES 
        if self.webClass not in ['NationalMap', 'SmallParty']:
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
                result.append(person)
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
            if IEvent.providedBy(item) and item.webApproved:
                result.append(item)
                continue
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
