from zope.interface import implementer
from zope.cachedescriptors.property import CachedProperty
from zope.interface import implementer

from dolmen.container import IBTreeContainer
from cromlech.security import getSecurityGuards, permissions
from dolmen.forms.base import Actions
from dolmen.forms.base import Fields
from dolmen.forms.base import action, name, context, form_component
from cromlech.browser.directives import title

from zopache.core.baseform import Form
from zope.interface import Interface
from zopache.core import Container
from zopache.crud import actions as formactions, i18n as _
from zopache.ttw import actions as ttwactions

from zopache.ttw.html import HTML
from .interfaces import IHTMLContainer
from zopache.ttw.html import TrustedHTML
from zopache.crud.forms import AddForm
from zopache.ttw.interfaces import IWeb    

@implementer(IHTMLContainer)
class HTMLContainer(TrustedHTML,Container):
    icon="ttwicons/Container.svg"
    webClass = "Container"
    def __init__(self):
        Container.__init__(self)



@form_component
@name (u'addContainer')
@context(IBTreeContainer)
@title("Add TTWContainer.")
@permissions('Manage')
@implementer(IWeb)
class ContainerAddForm(AddForm):
    subTitle = 'Add a Container'
    interface = Interface
    ignoreContent = True
    factory=HTMLContainer

    @CachedProperty
    def actions(self):
        return Actions(
              ttwactions.AddAndManage(_("Add and Manage","Add and Manage"), self.factory),
              ttwactions.AddAndCkEdit(_("Add and ckEdit","Add and CkEdit"), self.factory),
              ttwactions.AddAndAceEdit(_("Add and AceEdit","Add and AceEdit"), self.factory),
              formactions.Cancel(_("Cancel","Cancel")))        
