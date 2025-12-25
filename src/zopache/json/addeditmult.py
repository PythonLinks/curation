import json

from dolmen.container import IBTreeContainer

from zopache.pages.interfaces import IPageBase
from zopache.json.interfaces import IMultilingual,IMultilingualLeaf
from zopache.core.viewdecorators import *
from zopache.json.editjsonschema import AddJson, EditJson
from zopache.core.interfaces import ITreeSecurity
from zopache.business.jsonschemavalidator import JSONSchemaValidator
from zopache.json.multilingual import Multilingual, MultilingualLeaf

class LeafBase(object):
    def getSchema(self):
        schemaName = self.getSchemaName()        
        schema =  self.template[schemaName]
        result = schema.getAsDict()
        for item in result['properties'].values():
            item['required'].remove('description')
            del item['properties']['description']
        return result
    
@form_component
@name ('ckedit')
@context(IMultilingual)
@implementer(ITreeSecurity)
class EditMultilingual (EditJson):
    title = 'Edit this Multilingual Page.'
    subTitle = ''
    schemaName = "MultilingualSchema"  

@form_component
@name ('ckedit')
@context(IMultilingualLeaf)
@implementer(ITreeSecurity)
class EditMultilingualLeaf (LeafBase,EditJson):
    title = 'Edit this Multilingual Text.'
    subTitle = ''
    dataValidators = [JSONSchemaValidator]
    
@view_component
@name('addMultilingual')
@target(IView)
@context(IPageBase)
class AddMultilingual(AddJson):
    title = "Add a MultiLingual Page"
    subTitle = "You can add as many language versions as you need."
    factory = Multilingual
    schemaName = "MultilingualSchema"

    def newName(self,data):
        newName =  self.requestJsonDict['en']['title']
        newName = self.uniqueBothName(self.context, newName)
        return newName
        
    def dataModel(self):   
        contextJsonDict =  self.template['newMultilingualJson'].getAsDict()
        result = json.dumps(contextJsonDict)
        return result


@view_component
@name('addMultilingualLeaf')
@target(IView)
@context(IBTreeContainer)
class AddMultilingualLeaf(LeafBase,AddJson):
    title = "Add a MultiLingual Leaf"
    subTitle = ""
    factory = MultilingualLeaf
    schemaName = "MultilingualSchema"

    def newName(self,data):
        newName =  self.requestJsonDict['en']['title']
        return newName
        
    def dataModel(self):   
        contextJsonDict =  self.template['newMultilingualJson'].getAsDict()
        result = json.dumps(contextJsonDict)
        return result    

