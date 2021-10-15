import json

from zope import schema
from zope.interface import implementer
from dolmen.view import View
from cromlech.webob.response import Response
from dolmen.view import View, make_view_response

from dolmen.container import IBTreeContainer ,OrderedBTreeContainer

#PLEASE REMOVE THE NEXT LINE
from dolmen.container import  BTreeContainer

from zopache.core import Leaf
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.ttw.acescripts import AceScripts

from zopache.ttw.interfaces import IJSON, IJSONContainer
from zopache.ttw.javascript import JavascriptBase
from zopache.core.interfaces import ITreeSecurity
from zopache.core.viewdecorators import *

class AceScripts(AceScripts):
    aceMode = 'json'

@implementer(IJSON)
class JSON(JavascriptBase,Leaf):
    # NEEDS AN ICON
    icon="ttwicons/JSON.svg"
    source = "{}"
    
    def getSource(self):
        return self.getJavascript()

    def getAsString(self):
        return self.getJavascript()
    
    def asPythonObjects(self):
        return json.loads(self.source)
    
    def fromPythonObjects(self,data):
        self.source = json.dumps(data,indent=4)
        
    def getJavascript (self):
        return self.source
    
    def getAsDict(self):
        source = self.source           
        jsonDict = json.loads (source)
        return jsonDict
    
@implementer(IJSONContainer)
class JSONDict(JSON,OrderedBTreeContainer):
    title = ""
    description = ""
    source = "{}"
    def __init__(self):
        JSON.__init__(self)
        OrderedBTreeContainer.__init__(self)
        
    def getAsString(self):
        return json.dumps(self.getAsDict(),indent = 2)
    
    def getAsDict(self):
        source2 = self.source           
        json2 = json.loads (source2)

        properties = json2.get("properties",dict()) 
        for key,value  in self.items():
            if IJSON.providedBy(value):
               properties[key] = value.getAsDict()
        if properties:
            json2["properties"] = properties

        return json2
    
@implementer(IJSONContainer)
class JSONFolder(JSONDict):
    pass

@form_component
@name('addJSON')
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddJSON(AceScripts,AceAddForm):
    subTitle='Add a JSON Object'
    interface = IJSON
    ignoreContent = True
    factory=JSON

@form_component
@name('addJSONFolder')
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddJSONDict(AceScripts,AceAddForm):
    subTitle='Add a JSON Object'
    interface = IJSONContainer
    ignoreContent = True
    factory=JSONFolder
    
def makeJsonResponse(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or '')
        response.content_type=u'application/json'
        return response    

@view_component
@name('index')
@context(IJSON)
class Index(View):
    responseFactory = Response
    make_response = makeJsonResponse
        
    def render(self):
        return self.context.source


from zopache.business.imaporganization import IMapOrganization
from zopache.business.getjson import getStateJson

@view_component
@name('geojson')
@context(IMapOrganization)
class GEOIndex(View):
    responseFactory = Response
    make_response = makeJsonResponse
        
    def render(self):
        return getStateJson(self.context)
    
@view_component
@name('index')
@context(IJSONContainer)
class Index(View):
    responseFactory = Response
    make_response = makeJsonResponse
        
    def render(self):
        context = self.context.getAsString()
        return context
        

@form_component
@context(IJSON)
@name("aceedit")
@implementer(ITreeSecurity)
class AceEditJSON(AceScripts,AceEditForm):
    subTitle='Edit a JSON Object'
    interface = IJSON

"""
@form_component
@context(IJSON)
@name('manage')
@implementer(ITreeSecurity)
class ManageJSON(AceEditJSON):    
   pass
"""
from zopache.pages.interfaces import INotebook
@view_component
@name('source')
@context(INotebook)
class Source(View):
    responseFactory = Response
    make_response = makeJsonResponse
        
    def render(self):
               return self.context.source           

