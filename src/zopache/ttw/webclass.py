from zope.interface import implementer

from cromlech.security import getSecurityGuards, permissions
from dolmen.forms.base import action, name, context, form_component
from cromlech.browser.directives import title

from zopache.core import Container
from .interfaces import IWebClass, IProducts, IMoveableWebClass
from .container import ContainerAddForm
from zopache.ttw.interfaces import IWeb    
from zopache.core.getroot import getProducts
from zopache.core.interfaces import ITreeSecurity


class BaseWebClass (Container):
    title = "A Web Class"
    webClass = True #But not a string. 
    icon="ttwicons/Container.svg"
    def __init__(self):
        Container.__init__(self)

    def getFromWebClass(self, name, marker=None):
        result =self.get(name, marker)
        #IF THE WebCLASS CONTAINS THE OBJECT
        if result != marker:
            return result

        if IProducts.providedBy(self):
           return marker
        #AND NOW REPEAT THE LOOP WITH THE PARENT WEBCLASS
        if self.__parent__ == None:
            return marker
        return self.__parent__.getFromWebClass(name,marker)

    def postAddProcess(self,view=None):
        getProducts(self).indexTree()
        
    def postProcess(self,view = None):
        pass
    
@implementer(IMoveableWebClass)
class WebClass (BaseWebClass):
    pass

@implementer(IMoveableWebClass)
class ImutableWebClass (BaseWebClass):
    pass


@form_component
@name('addWebClass')
@context(IWebClass)
#@target(ITab)
@title("Add WebClass")
@implementer(ITreeSecurity)
class AddWebClass(ContainerAddForm):
    subTitle='Add a WebClass  (Manually Fix the ZClass)'
    interface = IWebClass
    ignoreContent = True
    factory=WebClass

from dolmen.view import name, context, view_component
from zopache.core.breadcrumbs import Breadcrumbs
from zopache.ttw.htmlviews import Index
@view_component
@name('index')
@context(IWebClass)
class WebClassIndex(Index,Breadcrumbs):           
    def render(self):
        return "This is the boring index view of a web class"
