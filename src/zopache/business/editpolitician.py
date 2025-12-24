import json
from dolmen.forms.base.errors import Error, Errors

from zopache.core.viewdecorators import *
from zopache.json.editjsonschema import AddJson, EditJson
from zopache.business.politician import Politician    
from zopache.business.interfaces import IPolitician
from zopache.core.interfaces import ITreeSecurity
from zopache.pages.interfaces import IPageBase

class PoliticianBase(object):

    def updateFromJsonDict(self,target,key,requestJsonDict):
        if key in requestJsonDict:
           value =  requestJsonDict[key]
           setattr(target,key,value)
           
    def contextJsonDict(self):
        contextJsonDict = dict()
        context = self.context
        
        #FIRST FOR THE ROOT FIELDS
        rootProperties = self.jsonSchemaDict["properties"]
        if 'introduction' in rootProperties:
            introduction = dict()
            contextJsonDict["introduction"] = introduction
            children = rootProperties["introduction"]["properties"].keys()
        
            for child in children:
                if hasattr(context,child):
                   value = getattr(context,child) 
                   introduction [child] = value
               
        children = list(self.jsonSchemaDict["properties"].keys())
        if 'introduction' in children: 
            children.remove('introduction')
        for child in children:
            if hasattr(context,child):
               value = getattr(context,child) 
               contextJsonDict [child] = value
        return contextJsonDict
    
    def applyData(self,data):
        target = self.target()
        rootProperties = self.jsonSchemaDict["properties"]
        
        if "introduction" in rootProperties:
           introductionKeys = (rootProperties
                                     ["introduction"]
                                     ["properties"].keys())
           requestIntroduction = self.requestJsonDict["introduction"]
           for key in introductionKeys:        
               self.updateFromJsonDict(target,key,requestIntroduction)


        rootKeys = rootProperties.keys()
        rootKeys = list(rootKeys)
        if "introduction" in rootProperties:        
           rootKeys.remove("introduction")
           
        requestJsonDict = self.requestJsonDict                
        for key  in rootKeys:
            if hasattr(target,key):
                delattr(target,key)
            self.updateFromJsonDict(target,key,requestJsonDict)
        target._p_changed = True
        return Errors()

    
class AddPolitician (PoliticianBase,AddJson):
    factory = Politician
    schemaName = "PoliticianSchema"
    
    def newName(self,data):
        newName =  self.requestJsonDict["introduction"]['title']
        return newName
    
@form_component
@name ('edit')
@context(IPolitician)
@implementer(ITreeSecurity)
class EditPolitician (PoliticianBase,EditJson):
    title = 'Edit this Person.'
    subTitle = 'Using JSON Schema.'
    schemaName = "PoliticianSchema"

@form_component
@name ('aceedit')
@context(IPolitician)
@implementer(ITreeSecurity)
class AceEditPolitician (EditPolitician):
      pass

    
@view_component
@name('addCandidate')
@target(IView)
@context(IPageBase)    
class AddCandidate(AddPolitician):

    title = "Add a Candidate"
    def dataModel(self):   
        contextJsonDict =  self.template['newCandidateJson'].getAsDict()
        del contextJsonDict["partyOfficer"]
        del contextJsonDict["electedOfficial"]           
        result = json.dumps(contextJsonDict)
        return result

           
@view_component
@name('addElectedOfficial')
@target(IView)
@context(IPageBase)    
class AddElectedOfficial(AddPolitician):
    title = "Add an Elected Official"
    def dataModel(self):   
        contextJsonDict =  self.template['newCandidateJson'].getAsDict()
        del contextJsonDict["partyOfficer"]
        result = json.dumps(contextJsonDict)
        return result
           
@view_component
@name('addPartyOfficer')
@target(IView)
@context(IPageBase)    
class AddPartyOfficer(AddPolitician):
    title = "Add a Party Officer"
    def dataModel(self):   
        contextJsonDict =  self.template['newCandidateJson'].getAsDict()
        del contextJsonDict["electedOfficial"]
        del contextJsonDict["candidateInfo"]           
        result = json.dumps(contextJsonDict)
        return result

