from zope.interface import implementer

from dolmen.container import IBTreeContainer
from zopache.business.subscribe import Member

from zopache.pages.location import LocationLeaf
from zopache.business.ipolitician import (IPolitician,
                                          IAddPolitician,
                                          IPoliticiansSite)
from zopache.pages.page import SiteRoot
from zopache.pages.interfaces import IPage
from zopache.business.imaginarypage import ImaginaryPage
from zopache.business.convert import Convert
@implementer (IPolitician)
class Politician (ImaginaryPage,LocationLeaf,Member,Convert):
    localOrNational = ""
    webClass = "Politician"
    clientClass = "category"
    def __init__(self):
        ImaginaryPage.__init__(self)
        LocationLeaf.__init__(self)
        Member.__init__(self)

    """    
    def getTitle(self):
        if 'title' in self.__dict__:
            return self.__dict__["title"]
        return self.content["title"]

    def setTitle(self,value):
        if 'title' in self.__dict__:
            self.__dict__["title"] = value
        self.content["title"] = value
    """
    
    def getDescription(self):
        if 'description' in self.__dict__:
            return self.__dict__["description"]
        return self.content["english"]["description"]

    def setDescription(self,value):
        if 'description' in self.__dict__:
            self.__dict__["description"] = value
        self.content["english"]["description"] = value

    def getSource(self):
        if 'source' in self.__dict__:
            return self.__dict__["source"]
        return self.content["english"]["source"]

    def setSource(self,value):
        if 'source' in self.__dict__:
            self.__dict__["source"] = value
        else:    
            self.content["english"]["source"] = value                

    #title = property(getTitle,setTitle)
    description = property(getDescription,setDescription)
    source = property(getSource,setSource)        

    def getConnect(self,arg):
        return self.getJsonValue('connect',arg)
    
    def getCandidateInfo(self,arg):
        return self.getJsonValue('candidateInfo',arg)
    
    def getElectedOfficial(self,arg):
        return self.getJsonValue('electedOfficial',arg)        

    def getPartyOfficer(self,arg):
        return self.getJsonValue('partyOfficer',arg)

    def getJsonValue(self,arg1,arg2):
        if hasattr(self,arg1):
           item1 = getattr(self,arg1) 
           if type( item1) == dict:
              if arg2 in item1:
                 return item1 [arg2]
        return ""     

    def isCandidate(self):
        return hasattr(self,'candidateInfo')

    def isElectedOfficial(self):
        return hasattr(self,'electedOfficial')

    def isPartyOfficer(self):
        return hasattr(self,'partyOfficer')

    def hasHistory(self):
        return hasattr(self,'history')

    def isNational(self):
        if not self.isCandidate():
           raise Exception("No Candidate Info")
        localOrNational = self.getCandidateInfo("localOrNational")
        return  'National' in localOrNational

    def isGreen(self):
        if self.isElectedOfficial():
            return True
        if not self.isCandidate():
           return False
        affiliation = self.getCandidateInfo("affiliation")
        if affiliation == 'Independent':
                return False
        if affiliation == 'Democrat':
                return False
        return True
    
    def isActive(self):
        return (self.isCandidate() or
                self.isElectedOffical() or
                self.isPartyOfficer())
    
from zopache.business.company import GeoBase        
@implementer (IPoliticiansSite)
class PoliticiansSite (LocationLeaf,SiteRoot):
    webClass = "Politician"
    clientClass = "category"    
    def __init__(self):
        SiteRoot.__init__(self)
        GeoBase.__init__(self)
        LocationLeaf.__init__(self)

    def setLatLng(self):
        pass
    
