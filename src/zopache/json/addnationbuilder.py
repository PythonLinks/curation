from zopache.core.viewdecorators import *
from zopache.json.editjsonschema import AddJson
from zopache.core.interfaces import ITreeSecurity
from zopache.pages.interfaces import IPageBase
from zopache.business.jsonschemavalidator import JSONSchemaValidator
from zopache.crud.addbyurl import AddByURLForm
from zopache.json.editjsonschema import Base

class AddBase (Base, AddByURLForm):
    dataValidators = [JSONSchemaValidator]

    def update(self):
        AddByURLForm.update(self)
        self.template = self.getTemplates()['json-editor']    

    def addUnauthorizedActions(self):    
           self.actions = Actions()

    def target(self):
        return self.new
    
@view_component
@name('addNBPage')
@target(IView)
@context(IPageBase)
class AddToNationBuilder(AddBase):
    title = "Add a Page to Nation Builder"
    subTitle = ""

    schemaName = "NBPageSchema"

    def newName(self,data):
        newName =  self.requestJsonDict["content"][0]['title']
        return newName
        
    def dataModel(self):
        return "{}"

    
