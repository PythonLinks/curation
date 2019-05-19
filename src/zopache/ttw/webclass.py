from zope.interface import implementer

from cromlech.security import getSecurityGuards, permissions
from dolmen.forms.base import action, name, context, form_component
from cromlech.browser.directives import title

from zopache.core import Container
from .interfaces import IWebClass, IProducts, IMutableWebClass
from .container import ContainerAddForm
from zopache.ttw.interfaces import IWeb    


class BaseWebClass (Container):
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
        return self.__parent__.getFromWebClass(name,marker)

        
    def postProcess(self):
        pass
    
@implementer(IWebClass)
class WebClass (BaseWebClass):
    pass

@implementer(IMutableWebClass)
class ImutableWebClass (BaseWebClass):
    pass


@form_component
@name('addWebClass')
@context(IWebClass)
#@target(ITab)
@title("Add WebClass")
@permissions('Manage')
@implementer(IWeb)
class AddWebClass(ContainerAddForm):
    subTitle='Add a WebClass  (Manually Fix the ZClass)'
    interface = IWebClass
    ignoreContent = True
    factory=WebClass
