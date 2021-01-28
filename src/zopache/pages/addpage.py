from dolmen.forms.base import Actions
from zopache.pages.pageactions import *
from zopache.crud.actions import Cancel
from zopache.pages.pageactions import *
from zopache.core.viewdecorators import *
from zopache.ttw.htmlviews import CkScripts
from zopache.ttw.htmlviews import AddCkHTMLBase

from zopache.core.uniquename import UniqueName
from zopache.crud.forms import AddByTitleForm
from zopache.pages.interfaces import (IMap,
                                      ILocation,
                                      IPage,
                                      IProxyPage,
                                      IAddLink,
                                      IActionNetwork)
from zopache.pages.page import Page, Link, ActionNetwork
from zopache.pages import Map, Location
from zopache.ttw.mail import Notify
from zopache.core.interfaces import ITreeSecurity
from zopache.business.exists import Duplicate
from zopache.forms.urlvalidator import DuplicateURLValidator
from zopache.pages.htmlvalidator import HTMLValidator
from zopache.pages.proxypage import ProxyPage
from zopache.core.getimage import getImage

class AddPageBase(
                  AddCkHTMLBase,
                  AddByTitleForm,
                  UniqueName,Notify):
    dataValidators = [Duplicate, DuplicateURLValidator, HTMLValidator]
    actions = Actions()

    def updateWidgets(self):
        AddByTitleForm.updateWidgets(self)
        
    def update(self):
        if self.treeSecurity():
           self.addAuthorizedActions()
        else:
           self.addUnauthorizedActions()

    def addUnauthorizedActions(self):
        self.actions = Actions()
               
    def addAuthorizedActions(self):       
        self.actions = Actions(
              AddAndView("Add and View", self.factory),
              AddAndAceEdit("Add and aceEdit", self.factory),
              AddAndCkEdit("Add and ckEdit", self.factory),
              Cancel("Cancel","Cancel"))
        
    def postAddProcess(self,view = None):
        self.new.postAddProcess (view = self)
        self.notifyAdminsNewPage()
            
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
    def postProcess(self):
        Link.postProcess(self.new, view = self)
        if 'form.field.imageURL' in self.request.response:
            getImage(self.new, self.request ['form.field.imageURL'])
  
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
    


    
