from dolmen.forms.base import Actions
from zopache.crud.actions import Cancel
from zopache.core.viewdecorators import *
from zopache.ttw.htmlviews import CkScripts
from zopache.ttw.htmlviews import AddCkHTMLBase
from zopache.crud.forms import AddByTitleForm, AddByNameForm
from zopache.crud.addbytitleactions import *

from zopache.pages.interfaces import (IMap,
                                      ILocation,
                                      IPage,
                                      ISiteRootPage,
                                      IProxyPage,
                                      IAddLink,
                                      IActionNetwork)
from zopache.pages.page import Page, Link, SiteRootPage, ActionNetwork
from zopache.pages import Map, Location
from zopache.core.interfaces import ITreeSecurity
from zopache.business.exists import Duplicate
from zopache.forms.urlvalidator import DuplicateURLValidator
from zopache.pages.htmlvalidator import HTMLValidator
from zopache.pages.proxypage import ProxyPage
from zopache.crud.getimage import getImage

class BaseAdd(AddCkHTMLBase):
    count = 0 
    layoutName = "UserMenu"
    actions = Actions()
    dataValidators = [Duplicate, DuplicateURLValidator, HTMLValidator]
    
        
    def addAuthorizedActions(self):           
        self.actions = Actions(
              AddByTitleAndView("Add and View", self.factory),
              AddByTitleAndAceEdit("Add and aceEdit", self.factory),
              AddByTitleAndCkEdit("Add and ckEdit", self.factory),
              AddByTitleAndManage("Add and Manage", self.factory),            
              Cancel("Cancel","Cancel"))

        
#THIS ONE SHOULD BE RETIRED 
class AddPageBase(BaseAdd, AddByTitleForm):
    def __init__(self,context,request):
        BaseAdd.__init__(self)
        AddByTitleForm.__init__(self,context,request)
 
class AddAuthorizedPage(AddPageBase):

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
    label="Add a ProxyPage"
    factory = ProxyPage    
    

@view_component
@name('addAction')
@target(IView)
@context(IPage)
@implementer(ITreeSecurity)
class AddAction(AddAuthorizedPage):
    interface = IActionNetwork
    label="Add a Remote Action"
    factory = ActionNetwork


@view_component
@name('addLink')
@target(IView)
@context(IPage)
@implementer(ITreeSecurity)
class AddLink(AddAuthorizedPage):
    interface = IAddLink
    title = "Add a Link"
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
    subTitle = 'Add a point on a map'
    factory = Location

    
#MAP
@view_component
@name('addSimpleMap')
@target(IView)
@context(IPage)    
@implementer(ITreeSecurity)
class AddMap(AddAuthorizedPage):
    subTitle = 'Add a map'
    interface = IMap
    label="Add a Map"
    factory = Map
    


    
