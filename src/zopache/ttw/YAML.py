import yaml 
from json import dumps

from zope.interface import implementer

from dolmen.view import View
from cromlech.webob.response import Response
from dolmen.view import View, make_view_response
from dolmen.container import IBTreeContainer 

from zopache.core import Leaf
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.ttw.acescripts import AceScripts
from zopache.ttw.interfaces import IJSON, IYAML
from zopache.core.interfaces import ITreeSecurity
from zopache.core.viewdecorators import *
from zopache.ttw.JSON import makeJsonResponse

class AceScripts(AceScripts):
    aceMode = 'yaml'

@implementer(IYAML)
class YAML(Leaf):
    icon="ttwicons/JSON.svg"
    source = ""
    json = ""
    
    def getSource(self):
        return self.source

    def getYAML(self):
        return self.source
    
    def getYAMLObject(self):    
        return yaml.safe_load(self.source) 

    def convertToJSON(self):
        return dumps (self.getYAMLObject())

    def getJSON(self):
        return self.json
    
    def getJavascript (self):
        return self.json
    
    def getAsDict(self):
        return self.getYAMLObject()
    
    def postProcess(self,view = None):
        self.json = self.convertToJSON()
        
    def postAddProcess(self,view = None):
        self.postProcess(self)
        
@form_component
@name('addYAML')
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddYAML(AceScripts,AceAddForm):
    subTitle='Add a YAMLObject'
    interface = IYAML
    ignoreContent = True
    factory=YAML

@view_component
@name('index')
@context(IYAML)
class Index(View):
    responseFactory = Response
    make_response = makeJsonResponse
        
    def render(self):
        return self.context.json

@form_component
@context(IYAML)
@name("aceedit")
@implementer(ITreeSecurity)
class AceEditYAML(AceScripts,AceEditForm):
    subTitle='Edit a JSON Object'
    interface = IYAML
    
@view_component
@name('source')
@context(IYAML)
class Source(View):
    def render(self):
               return self.context.source
           
