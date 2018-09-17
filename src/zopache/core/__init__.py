#This is a package. 
from zope.i18nmessageid import MessageFactory
i18n = MessageFactory("zopache.core")
from cromlech.browser.interfaces import IPublicationRoot
from os import path
from dolmen.template import TALTemplate
from dolmen.view import View, make_layout_response
from cromlech.webob.response import Response
from dolmen.container import BTreeContainer

from cromlech.location import get_absolute_url
from cromlech.container.contained import Contained
from persistent import Persistent
class Leaf(Contained, Persistent):
    icon=''
    def postProcess(self):
        pass

from dolmen.container import BTreeContainer
class Container(BTreeContainer):
    icon=''
    def postProcess(self):
        pass

class RootContainer (BTreeContainer):
    def __init__(self):
       BTreeContainer.__init__(self)

       #Needed For Cut Copy Paste
       self.pasteFolder=BTreeContainer()
       
TEMPLATE_DIR = path.join(path.dirname(__file__), 'templates')
def tal_template(name):
    return TALTemplate(path.join(TEMPLATE_DIR, name))

class Page(View):
        responseFactory = Response
        make_response = make_layout_response

        def url(self):
           return get_absolute_url(self.context, self.request)
                        
from cromlech.browser.interfaces import IPublicationRoot                        
def getRoot(object):
        max = 9999
        context=object
        while context is not None:
            if IPublicationRoot.providedBy(context):
                return context
            context = context.__parent__
            max -= 1
            if max < 1:
                raise TypeError("Maximum location depth exceeded, "                                "probably due to a a location cycle.")
        raise TypeError("Parents needed to  determine location root")


class ErrorPage(Page):
    code = 400

    def make_response(self, *args, **kws):
        response = make_layout_response(self, *args, **kws)
        response.status_code = self.code
        return response
