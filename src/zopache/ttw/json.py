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



@implementer(IJSON)
class JSON(Leaf):
    # NEEDS AN ICON
    icon="ttwicons/JSON.svg"
    def asPythonObjects(self):
        return json.loads(self.source)
    
    def fromPythonObjects(self,data):
        self.source = json.dumps(data)
        
    def getJavascript (self):
        return self.source
    
class  AceScripts(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/json");
        </script>
        """
    

@form_component
@name('addJSON')
@context(IBTreeContainer)
@title("Add JSON")
@permissions('Manage')
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
@title("View JSON")
class Index(View):
    responseFactory = Response
    make_response = makeResponse
        
    def render(self):
               return self.context.source


@form_component
@context(IJSON)
@title("AceEdit JSON")
@name("aceedit")
@permissions('Manage')
class AceEditJSON(AceScripts,AceEditForm):
    subTitle='Edit a JSON Object'

    def postProcess(self):
        pass




@form_component
@context(IJSON)
@name('manage')
@title("Manage")
@permissions('Manage')
class ManageJSON(AceEditJSON):    
   pass
