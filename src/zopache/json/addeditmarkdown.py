import json

from dolmen.container import IBTreeContainer

from zopache.pages.interfaces import IPageBase
from zopache.json.interfaces import IMarkdown
from zopache.core.viewdecorators import *
from zopache.json.editjsonschema import AddJson, EditJson
from zopache.core.interfaces import ITreeSecurity
from zopache.business.jsonschemavalidator import JSONSchemaValidator
from zopache.json.markdown import JSONMarkdown

@form_component
@name ('edit')
@context(IMarkdown)
@implementer(ITreeSecurity)
class EditMarkdown (EditJson):
    title = 'Edit this Multilingual Page.'
    subTitle = ''
    schemaName = "JSONMarkdownSchema"  

@view_component
@name('addJSONMarkdown')
@target(IView)
@context(IPageBase)
class AddMarkdown(AddJson):
    title = "Add a Markdown Page"
    subTitle = ""
    factory = JSONMarkdown
    schemaName = "JSONMarkdownSchema"

    def newName(self,data):
        newName = self.requestJsonDict['title']
        newName = self.uniqueBothName(self.context, newName)        
        return newName
    
    def dataModel(self):   
        contextJsonDict =  {}
        result = json.dumps(contextJsonDict)
        return result


