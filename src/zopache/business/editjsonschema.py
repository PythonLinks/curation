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
from zopache.crud.actions import AddByJSON, AddByJsonAndEdit,Cancel
from zopache.business.exists import Duplicate
from zopache.business.interfaces import IClass
    
class Base(object):
    interface = IClass
    fields = Fields(IClass)

    def contextJsonDict(self):
        return self.context.json

    @property
    def jsonSchemaDict(self):
            result =  self.template[self.schemaName]
            result = result.getAsDict()
            return result
    
    def jsonSchemaString(self):
        result =  self.template[self.schemaName]        
        result = result.getAsString()
        return result

    def footerScripts(self):
        return ""

    def options(self):
        return ""
    
    def applyData(self,data):
        target = self.target()
        target.json =  self.requestJsonDict
        target._p_changed = True
        return Errors()
    
class AddJson (Base, AddAnonymousPage):
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
              AddByJsonAndEdit("Add and CME Edit", self.factory),
              Cancel("Cancel","Cancel"))
    
class EditJson( Base,EditForm):
    dataValidators = [JSONSchemaValidator]
    
    def contextJsonDict(self):
        return self.context.json
    
    def acquireTitle(self):
        return 'Edit ' + self.context.title

    def target(self):
        return self.context
    
    def update(self):
        products = self.getProducts()
        self.template = self.getTemplates()['json-editor']    
        EditForm.update(self)

    def contextJsonString(self):
        if hasattr(self,'submissionError') and len(self.submissionError):
           return self.requestJsonString
        else:
           return json.dumps(self.contextJsonDict())





