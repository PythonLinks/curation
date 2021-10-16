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
from zopache.crud import update  as updateactions
from zopache.ttw import actions as ttwactions

from zopache.ttw.html import HTML
from .interfaces import IHTMLContainer, IAceContainer
from zopache.ttw.html import TrustedHTML
from zopache.crud.forms import TreeSecurityAddForm
from zopache.ttw.interfaces import IWeb    
from zopache.core.interfaces import ITreeSecurity
from zopache.ttw.addeditforms import AceAddForm

@implementer(IHTMLContainer)
class HTMLContainer(TrustedHTML,Container):
    icon="ttwicons/Container.svg"
    webClass = "Container"
    def __init__(self):
        Container.__init__(self)

@implementer(IAceContainer)
class AceContainer(TrustedHTML,Container):
    icon="ttwicons/Container.svg"
    def __init__(self):
        Container.__init__(self)        


@form_component
@name (u'addContainer')
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class ContainerAddForm(TreeSecurityAddForm):
    subTitle = 'Add a WYSIWYG HTML Folder'
    interface = Interface
    ignoreContent = True
    factory=HTMLContainer

    @property
    def actions(self):
         return Actions(
              ttwactions.AddAndManage(_("Add and Manage","Add and Manage"), self.factory),
              ttwactions.AddAndCkEdit(_("Add and ckEdit","Add and CkEdit"), self.factory),
              ttwactions.AddAndAceEdit(_("Add and AceEdit","Add and AceEdit"), self.factory),
              formactions.Cancel(_("Cancel","Cancel")))        

from zopache.ttw.htmlviews import AddAceHTML
@form_component
@name (u'addAceFolder')
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AceContainerAddForm(AddAceHTML):
    subTitle = 'Add an Ace HTML Folder'
    interface = IAceContainer
    ignoreContent = True
    factory=AceContainer

    def authorizedActions(self):
        self.actions = Actions(
              ttwactions.AddAndManage(_("Add and Manage","Add and Manage"), self.factory),
              ttwactions.AddAndAceEdit(_("Add and AceEdit","Add and AceEdit"), self.factory),
              formactions.Cancel(_("Cancel","Cancel")))        
    
import crom
from zopache.zmi.interfaces import IURLSegment
@crom.adapter
@crom.sources(IAceContainer)
@crom.target(IURLSegment)
class IAceContainerAdaptor(object):
    def __init__(self,context):
        self.context=context   

    def getSegment(self):
        return 'manage'
