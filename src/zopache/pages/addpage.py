from dolmen.forms.base import Actions
from zopache.crud.actions import Cancel
from zopache.core.viewdecorators import *
from zopache.ttw.htmlviews import CkScripts
from zopache.ttw.htmlviews import AddCkHTMLBase
from zopache.crud.forms import AddByTitleForm, AddByNameForm
from zopache.crud.addbytitleactions import *
from dolmen.forms.base import Fields
from zopache.pages.interfaces import (IMap,
                                      ILocation,
                                      IPage,
                                      ISiteRootPage,
                                      IProxyPage,
                                      IAddLink,
                                      IActionNetwork)
from zopache.pages.page import Page, Link, SiteRootPage, ActionNetwork
from zopache.pages.location import SimpleMap, Location
from zopache.core.interfaces import ITreeSecurity
from zopache.business.exists import Duplicate
from zopache.forms.urlvalidator import DuplicateURLValidator
from zopache.pages.htmlvalidator import HTMLValidator
from zopache.pages.proxypage import ProxyPage
from zopache.crud.getimage import getImage
from zopache.ttw.mail import Notify

class BaseAdd(AddCkHTMLBase,AddByTitleForm,Notify):
    count = 0 
    layoutName = "UserMenu"
    actions = Actions()
    dataValidators = [Duplicate, DuplicateURLValidator, HTMLValidator]
    def __init__(self,context,request):
        #First give it a context, then initialize Notify.
        AddByTitleForm.__init__(self,context,request)
        Notify.__init__(self)
    
    @property
    def fields(self):
        return  Fields(self.interface)    
        
    def addAuthorizedActions(self):           
        self.actions = Actions(
              AddByTitleAndView("Add and View", self.factory),
              AddByTitleAndAceEdit("Add and aceEdit", self.factory),
              AddByTitleAndCkEdit("Add and ckEdit", self.factory),
              AddByTitleAndManage("Add and Manage", self.factory),            
              Cancel("Cancel","Cancel"))

#class AddPageBase( BaseAdd):
#     pass
 
class AddAuthorizedPage(BaseAdd):

    actions = Actions()

    def getSubTitle(self):
          return (
                "To a " +  
                self.context.webClass +
                u' called: ' +
                self.context.getTitle()
               )
          
@view_component
@name('addPage')
@target(IView)
@context(IPage)
@implementer(ITreeSecurity)
class AddPage(AddAuthorizedPage):
    title = "Add a Web Page"
    subTitle = "It can have child pages."
    interface = IPage
    label="Add a Wiki Page"
    factory = Page

from zopache.application.interfaces import IRootContainer
@view_component
@name('addRootPage')
@target(IView)
@context(IRootContainer)
@implementer(ITreeSecurity)
class AddRootPage(AddAuthorizedPage):
    title = "Add a Root Page"
    subTitle = "This can be a whole new website.  Only at the top of the tree."
    dataValidators = []
    interface = ISiteRootPage
    label="Add a Root Wiki Page"
    factory = SiteRootPage
    
@view_component
@name('addProxyPage')
@target(IView)
@context(IPage)
@implementer(ITreeSecurity)
class AddProxyPage(AddAuthorizedPage):
    interface = IProxyPage
    title="Add a ProxyPage"
    subTitle = "This displays content from another page."
    factory = ProxyPage    
    

@view_component
@name('addAction')
@target(IView)
@context(IPage)
@implementer(ITreeSecurity)
class AddAction(AddAuthorizedPage):
    interface = IActionNetwork
    title = "Add a Remote Action"
    factory = ActionNetwork


@view_component
@name('addLink')
@target(IView)
@context(IPage)
@implementer(ITreeSecurity)
class AddLink(AddAuthorizedPage):
    interface = IAddLink
    title = "Add a Link"
    subTitle = "Refering to a remote page."
    factory = Link
  
#LOCAION
@view_component
@name('addLocation')
@target(IView)
@context(IMap)
@implementer(ITreeSecurity)
class AddLocation(AddAuthorizedPage):
    interface = ILocation
    label="Add a Location"
    subTitle = 'These points show up on parent maps. '
    factory = Location

    
#MAP
@view_component
@name('addSimpleMap')
@target(IView)
@context(IPage)    
@implementer(ITreeSecurity)
class AddMap(AddAuthorizedPage):
    subTitle = 'Add a map'
    subTitile = 'Remember to enable map tokens.'
    interface = IMap
    label="Add a Map"
    factory = SimpleMap
    


    
