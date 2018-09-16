from zope.interface import implementer

from cromlech.security import getSecurityGuards, permissions
from dolmen.forms.base import action, name, context, form_component
from cromlech.browser.directives import title

from zopache.core import Container
from .interfaces import IWebClass, IProducts
from .container import ContainerAddForm
from zopache.ttw.interfaces import IWeb    

@implementer(IWebClass)
class WebClass (Container):
    icon="ttwicons/Container.svg"
    title = ""
    def __init__(self):
        Container.__init__(self)
        
    def postProcess(self):
        pass

@implementer(IWebClass)
class ImutableWebClass (Container):
    icon="ttwicons/Container.svg"
    title = ""
    def __init__(self):
        Container.__init__(self)
        

@form_component
@name('addWebClass')
@context(IProducts)
#@target(ITab)
@title("Add WebClass")
@permissions('Manage')
@implementer(IWeb)
class AddWebClass(ContainerAddForm):
    subTitle='Add a WebClass  (Manually Fix the ZClass)'
    interface = IWebClass
    ignoreContent = True
    factory=WebClass
