#This software is subject to the No Compete MIT license License Agreement.

from zopache.core.viewdecorators import *
from zope import schema
from cromlech.webob.response import Response

from dolmen.view import View, make_view_response

from dolmen.container import IBTreeContainer

from zopache.core import Leaf
from zopache.ttw.interfaces import ISourceLeaf
from zopache.ttw.interfaces import ITestSource as ISource
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from zopache.crud.forms import EditDemoForm
from zopache.ttw.acescripts import AceScripts


class ICSS(ISourceLeaf):
    """Basic CSS CRUD"""

    title = schema.TextLine(
        title = u'Title',
        description = u'Please Describe this CSS.',
        required = False,
    )

    source= schema.Text(
        title = u'CSS Source Code',
        description = u'The CSS goes here.',
        required = False,
        default = u'',
    )


@implementer(ICSS)
class CSS(Leaf):
    icon="ttwicons/CSS.svg"

class  AceScripts(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/css");
        </script>
        """
    

@form_component
@name('addCSS')
@context(IBTreeContainer)
@title("Add CSS")
@permissions('Manage')
class AddCSS(AceScripts,AceAddForm):
    subTitle='Add a CSS Object'
    interface = ICSS
    ignoreContent = True
    factory=CSS
    

def make_css_response(view, result, *args, **kwargs):
        response = view.responseFactory()
        response.write(result or u'')
        response.content_type=u'text/css'
        return response    

@view_component
@name('index')
@context(ICSS)
@title("View CSS")
class Index(View):
    responseFactory = Response
    make_response = make_css_response
        
    def render(self):
               return self.context.source

#HERE IS THE ACE EDIT FORM
@form_component
@context(ICSS)
@title("AceEdit")
@name("aceedit")
@permissions('Manage')
class AceEditCSS(AceScripts,AceEditForm):
    subTitle='Edit a CSS Object'


#AND HERE IS THE ACE DEMO FORM
@form_component
@context(ICSS)
@title("Ace Demo")
@name("acedemo")
class AceDemoCSS(AceScripts,EditDemoForm):
    subTitle='Edit a CSS Object'


@form_component
@context(ICSS)
@name('manage')
@title("Manage")
@permissions('Manage')
class ManageCSS(AceEditCSS):    
   pass
