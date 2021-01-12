import googlemaps
import json
from zopache.crud import actions as formactions
from zope.interface import Interface
from zope.schema._field import Choice
from zope import schema

from cromlech.browser.exceptions import HTTPFound
from dolmen.forms.base.errors import Error, Errors
from dolmen.forms.base import Action, Actions, SuccessMarker

from zopache.core.viewdecorators import *
from zopache.crud.forms import EditForm
from zopache.pages.interfaces import IPage
from zopache.core.interfaces import ITreeSecurity
from zopache.business.jsonschemavalidator import JSONSchemaValidator
from zopache.pages.addanonymous import AddAnonymousPage
from zopache.business.politician import Politician    
from zopache.crud.actions import AddByJSON, AddByJsonAndEdit,Cancel
from zopache.business.ipolitician import IPolitician
from zopache.business.exists import Duplicate

class IClass(Interface):

    json= schema.Text(
        title = 'Json Data',
        required = True,
        default = '{}',
    )         

class Base(object):
    interface = IClass
    fields = Fields(IClass)



    @property
    def jsonSchemaDict(self):
            result =  self.context.webClassAcquire["json-schema"]
            result = result.getAsDict()
            return result
    
    def jsonSchemaString(self):
        result =  self.webClassAcquire["json-schema"]
        result = result.getAsString()
        return result

    def updateFromJsonDict(self,target,key,requestJsonDict):
        if key in requestJsonDict:
           value =  requestJsonDict[key]
           setattr(target,key,value)
        
    def applyData(self):

        target = self.target()
        children = (self.jsonSchemaDict["properties"]["introduction"]["properties"].keys())
        requestJsonDict = self.requestJsonDict["introduction"]
        for key in children:        
            self.updateFromJsonDict(target,key,requestJsonDict)
        
        children = list(self.jsonSchemaDict["properties"].keys())
        children.remove("introduction")
        requestJsonDict = self.requestJsonDict
        for key  in children:
            if hasattr(target,key):
                delattr(target,key)
            self.updateFromJsonDict(target,key,requestJsonDict)
        self.context._p_changed = True
        return Errors()

    def footerScripts(self):
        return ""


class AddBase (Base, AddAnonymousPage):
    dataValidators = [JSONSchemaValidator, Duplicate]

    def update(self):
        AddAnonymousPage.update(self)
        self.template = self.getTemplates()['json-editor']    

    #IF THERE IS A DATA VALIDATION ERROR
    #RETURN THE SUBMITTED JSON
    #ELSE RETURN THE DEFAULT JSON
    def contextJsonString(self):
        if hasattr(self,'submissionError') and len(self.submissionError):
           return self.requestJsonString
        else:
           return self.dataModel()


    def addUnauthorizedActions(self):    
           self.actions = Actions(
                  formactions.AddByJSON("Add and View", self.factory),
                  formactions.Cancel("Cancel","Cancel"))

    def target(self):
        return self.new
    
    def addAuthorizedActions(self):       
        self.actions = Actions(
              AddByJSON("Add and View", self.factory),
              #AddByJsonAndEdit("Add and CME Edit", self.factory),
              Cancel("Cancel","Cancel"))

class AddPolitician (AddBase):
    factory = Politician    
        
class EditBase( Base,EditForm):
    dataValidators = [JSONSchemaValidator]

    def acquireTitle(self):
        return 'Edit ' + self.context.title

    def target(self):
        return self.context
    
    def update(self):
        products = self.getProducts()
        self.template = self.getTemplates()['json-editor']    
        EditForm.update(self)

    def contextJsonDict(self):
        contextJsonDict = dict()
        introduction = dict()
        contextJsonDict["introduction"] = introduction
        context = self.context
        
        #FIRST FOR THE ROOT FIELDS
        children = self.jsonSchemaDict["properties"]["introduction"]["properties"].keys()
        for child in children:
            if hasattr(context,child):
               value = getattr(context,child) 
               introduction [child] = value
               
        children = list(self.jsonSchemaDict["properties"].keys())
        children.remove('introduction')
        for child in children:
            if hasattr(context,child):
               value = getattr(context,child) 
               contextJsonDict [child] = value
        return contextJsonDict

    def contextJsonString(self):
        if hasattr(self,'submissionError') and len(self.submissionError):
           return self.requestJsonString
        else:
           return json.dumps(self.contextJsonDict())


@form_component
@name ('ckedit')
@context(IPolitician)
@implementer(ITreeSecurity)
class EditPolitician (EditBase):
    title = 'Edit this Person.'
    subTitle = 'Using JSON Schema.'
       
@form_component
@name ('aceedit')
@context(IPolitician)
@implementer(ITreeSecurity)
class AceEditPolitician (EditPolitician):
      pass
  
       
@view_component
@name('addCandidate')
@target(IView)
@context(IPage)    
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
@context(IPage)    
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
@context(IPage)    
class AddPartyOfficer(AddPolitician):
    title = "Add a Party Officer"
    def dataModel(self):   
        contextJsonDict =  self.template['newCandidateJson'].getAsDict()
        del contextJsonDict["electedOfficial"]
        del contextJsonDict["candidateInfo"]           
        result = json.dumps(contextJsonDict)
        return result
        
