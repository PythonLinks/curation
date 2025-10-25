import json

from dolmen.container import IBTreeContainer

from zopache.pages.interfaces import IPageBase
from zopache.json.interfaces import IBasicJSON
from zopache.core.viewdecorators import *
from zopache.json.editjsonschema import AddJson, EditJson
from zopache.core.interfaces import ITreeSecurity
from zopache.business.jsonschemavalidator import JSONSchemaValidator
from zopache.json.basic import BasicJSON


@form_component
@name ('ckedit')
@context(IBasicJSON)
@implementer(ITreeSecurity)
class EditBasicJSON (EditJson):
    title = 'Edit this Tracking Page.'
    subTitle = ''
    schemaName = "BasicSchema"  

    
@view_component
@name('addBase')
@target(IView)
@context(IPageBase)
class AddBase(AddJson):
    title = "Add a Tracking Page"
    subTitle = "To Track Mastodon vs Twitter"
    factory = BasicJSON
    schemaName = "BasicSchema"

    def newName(self,data):
        newName =  self.requestJsonDict['title']
        newName = self.uniqueBothName(self.form.context, newName)        
        return newName
        
