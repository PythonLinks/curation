#This software is subject to the CV License Agreement.

from zope.cachedescriptors.property import CachedProperty
from zope import interface
from zope import schema
from zope.schema.interfaces import IField
from zope.interface import Interface
from zope.interface import implementer

from dolmen.forms.base import action, name, context, form_component
from crom import target, order
from cromlech.browser.directives import title
from cromlech.security import permissions
from dolmen.view import name, context, view_component
from dolmen.view import View
from cromlech.webob.response import Response
from dolmen.view import View, make_view_response

from dolmen.container import IBTreeContainer
from dolmen.forms.base import Actions


from zopache.crud import actions as formactions, i18n as _
from zopache.core import Leaf
from zopache.ttw.interfaces import IWeb
from zopache.ttw.interfaces import ISourceLeaf
from zopache.ttw.interfaces import ISource
from zopache.ttw.addeditforms import AceAddForm, AceEditForm
from .interfaces import ITestURL

from cromdemo.interfaces import ITab

class ICSSBase(ISourceLeaf):
    """Basic CSS FORM with CRUD"""

    title = schema.TextLine(
        title = u'Title',
        description = u'A short reminder of what this CSS page does or its versin name.',
        required = False,
    )

    source= schema.Text(
        title = u'CSS Source Code',
        description = u'The CSS goes here.',
        required = False,
        default = u'',
    )

# just so the test url would be last.     
class ICSS(ICSSBase,ITestURL):
    pass


@implementer(ICSS)
class CSS(Leaf):
    icon="ttwicons/CSS.svg"
    def commands(self,view):
        url=view.url(self)
        index=view.liHref(url+'/index','View')
        manual=view.liHref('http://www.zopache.com/baseicwebobjects/css','CSS Manual')
        return index + manual 
                

from zopache.ttw.acescripts import AceScripts
class  AceScripts(AceScripts):
    def  footerScripts(self):
        return self.aceEditorFooter + """ 
        <script >editor.getSession().setMode("ace/mode/css");
        </script>
        """
    

@form_component
@name('addCSS')
@context(IBTreeContainer)
#@target(ITab)
@title("Add CSS")
@permissions('Manage')
@implementer(IWeb)
class AddCSS(AceScripts,AceAddForm):
    subTitle='Add a CSS Object'
    interface = ICSS
    ignoreContent = True
    factory=CSS
    
 #   def footerScripts(self):
 #       return AceScripts.footerScripts(self)

#    def headerScripts(self):
#          return AceScripts.headerScripts(self)    
    
    def commands(self):
        manual=self.liHref('http://www.zopache.com/baseicwebobjects/css','CSS Manual')
        return manual 


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


@form_component
@context(ICSS)
@target(ITab)
@title("AceEdit")
@name("aceedit")
@permissions('Manage')
class AceEditCSS(AceScripts,AceEditForm):
    subTitle='Edit a CSS Object'

    def postProcess(self):
        pass




@form_component
@context(ICSS)
@target(ITab)
@name('manage')
@implementer(IWeb)
@title("Manage")
@permissions('Manage')
class ManageCSS(AceEditCSS):    
   pass
