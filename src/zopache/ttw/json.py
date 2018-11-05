#This software is subject to the No Compete MIT license License Agreement.

from zopache.core.viewdecorators import *
from zopache.application.interfaces import ITab
from zope import schema
from zope.interface import implementer

from dolmen.view import View
from cromlech.webob.response import Response
from dolmen.view import View, make_view_response

from dolmen.container import IBTreeContainer

from zopache.core import Leaf
from zopache.ttw.interfaces import ISourceLeaf
from zopache.ttw.interfaces import ISource
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.ttw.acescripts import AceScripts


class IJSON(Interface):
    """Basic JSON CRUD """

    title = schema.TextLine(
        title = u'Title',
        description = u'Please Describe this JSON.',
        required = False,
    )

    source= schema.Text(
        title = u'JSON Source',
        description = u'The JSON  goes here.',
        required = False,
        default = u'',
    )


@implementer(IJSON)
class JSON(Leaf):
    # NEEDS AN ICON
    #icon="ttwicons/CSS.svg"
    pass

class  AceScripts(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/json");
        </script>
        """
    

@form_component
@name('addJSON')
@context(IBTreeContainer)
#@target(ITab)
@title("Add JSON")
@permissions('Manage')
class AddCSS(AceScripts,AceAddForm):
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
@crom.target(ITab)
@title("AceEdit JSON")
@name("aceedit")
@permissions('Manage')
class AceEditJSON(AceScripts,AceEditForm):
    subTitle='Edit a JSON Object'

    def postProcess(self):
        pass




@form_component
@context(IJSON)
@crom.target(ITab)
@name('manage')
@title("Manage")
@permissions('Manage')
class ManageJSON(AceEditJSON):    
   pass
