import json
from zope.interface import Interface

from zope.interface import implementer
from dolmen.forms.base.errors import Error, Errors
from dolmen.container import BTreeContainer,IBTreeContainer
from dolmen.forms.base import Actions

from zopache.crud import actions as formactions, i18n as _
from zopache.ttw import actions as ttwactions
from zopache.ttw.interfaces import IDeletable
from zopache.core.viewdecorators import *
from zopache.json.editjsonschema import AddJson, EditJson
from zopache.json.editjsonschema import IClass
from zopache.crud.forms import AddForm
from zopache.core.interfaces import ITreeSecurity
from zopache.ttw.JSON import JSONFolder

from zopache.core import Container

class ISchemaClass(IClass,IDeletable):
    pass

@implementer(ISchemaClass)
class SchemaClass(Container):
    json = {}
    def __init__(self):
        BTreeContainer.__init__(self)
        schema = JSONFolder()
        schema.source = '{"title","Hello World!"}'
        self['schema'] = schema
        
    @property
    def title(self):
        try:
            title = self.json["title"]
        except:
            title = "JSON Schema Assignment"        
        return title
    
@form_component
@name ('ckedit')
@context(ISchemaClass)
@implementer(ITreeSecurity)
class EditSchemaClass (EditJson):
    title = 'Edit this Object.'
    subTitle = 'The Form is defined by its child JSON Schema.'
    
    def update(self):
        EditJson.update(self)
        self.template = self.getTemplates()['json-editor']
        
    @property
    def jsonSchemaDict(self):
        result =  self.context['schema']
        result = result.getAsDict()
        return result
    
    @property
    def jsonSchemaString(self):
        result =  self.context['schema']
        result = result.getAsString()
        return result        
    
@view_component
@name('addSchemaClass')
@target(IView)
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddSchemaClass(AddForm):
    title = "Add an object defined with a JSON Schema"
    subTitle = "The schema will be underneath the created object."
    factory = SchemaClass
    interface = Interface
    
    @property
    def actions(self):
         return Actions(
              ttwactions.AddAndManage(_("Add and Manage","Add and Manage"), self.factory),
              ttwactions.AddAndCkEdit(_("Add and ckEdit","Add and CkEdit"), self.factory),
              formactions.Cancel(_("Cancel","Cancel")))        

    def newName(self,data):
        newName =  data['__name__']
        return newName
        
    def dataModel(self):
        return {}

from zopache.ttw.JSON import makeJsonResponse
from zopache.core.view import View
@view_component
@name('index')
@context(ISchemaClass)
class Index(View):
    make_response = makeJsonResponse
        
    def render(self):
        return json.dumps(self.context.json,indent = 4)

