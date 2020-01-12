import json

from zopache.core.viewdecorators import *
from zope import schema
from zope.interface import implementer
from dolmen.view import View
from cromlech.webob.response import Response
from dolmen.view import View, make_view_response

from dolmen.container import IBTreeContainer

from zopache.core import Leaf
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.ttw.acescripts import AceScripts

from zopache.ttw.interfaces import IJSON
from zopache.ttw.javascript import JavascriptBase
from zopache.core.interfaces import ITreeSecurity

@implementer(IJSON)
class JSON(JavascriptBase,Leaf):
    # NEEDS AN ICON
    icon="ttwicons/JSON.svg"

    def getSource(self):
        return self.getJavascript()
    
    def asPythonObjects(self):
        return json.loads(self.source)
    
    def fromPythonObjects(self,data):
        self.source = json.dumps(data)
        
    def getJavascript (self):
        return self.source
#        start = "var " + self.__name__ + ' = "" + "'
#        end = '";'
#        return start + self.source  + end
        
    
class  AceScripts(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/json");
        </script>
        """
    

@form_component
@name('addJSON')
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddJSON(AceScripts,AceAddForm):
    subTitle='Add a JSON Object'
    interface = IJSON
    ignoreContent = True
    factory=JSON
    

def makeResponse(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or u'')
        response.content_type=u'application/json'
        return response    

@view_component
@name('index')
@context(IJSON)
class Index(View):
    responseFactory = Response
    make_response = makeResponse
        
    def render(self):
               return self.context.source


@form_component
@context(IJSON)
@name("aceedit")
@implementer(ITreeSecurity)
class AceEditJSON(AceScripts,AceEditForm):
    subTitle='Edit a JSON Object'

    def postProcess(self):
        pass




@form_component
@context(IJSON)
@name('manage')
@implementer(ITreeSecurity)
class ManageJSON(AceEditJSON):    
   pass

from zopache.pages.interfaces import INotebook
@view_component
@name('source')
@context(INotebook)
class Source(View):
    responseFactory = Response
    make_response = makeResponse
        
    def render(self):
               return self.context.source           

