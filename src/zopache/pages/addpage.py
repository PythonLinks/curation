
from dolmen.forms.base import Actions
from zopache.pages.pageactions import *
from zopache.crud import actions as formactions
from zopache.pages.pageactions import *
from zopache.core.viewdecorators import *
from zopache.ttw.htmlviews import CkScripts
from zopache.ttw.htmlviews import AddCkHTMLBase

from zopache.core.uniquename import UniqueName
from zopache.crud.forms import AddByTitleForm, AddByURLForm
from zopache.pages.interfaces import IMap, ILocation, IPage
from zopache.pages.page import Page
from zopache.pages import Map, Location
from zopache.ttw.mail import Notify
from zopache.core.interfaces import ITreeSecurity
from zopache.business.exists import Duplicate

class AddPageBase(AddByTitleForm,AddCkHTMLBase,UniqueName,Notify):
    dataValidators = [Duplicate]
    
    def postAddProcess(self,view = None):
        self.new.postAddProcess (view = self)
        self.notifyAdminsNewPage()
            
class AddAuthorizedPage(AddPageBase):
    actions = Actions()
    def update(self):
        if self.treeSecurity():
            self.setActions()

    def getSubTitle(self):
          return (
                "To a " +  
                self.context.webClass +
                u' called: ' +
                self.context.getTitle()
               )
      
    def setActions(self):       
        self.actions = Actions(
              AddAndView("Add and View", self.factory),
              AddAndCkEdit("Add and ckEdit", self.factory),
              AddAndAceEdit("Add and AceEdit", self.factory),
              formactions.Cancel("Cancel","Cancel"))
            
@view_component
@name('addPage')
@target(IView)
@context(IPage)
@implementer(ITreeSecurity)
class AddPage(AddAuthorizedPage):
    interface = IPage
    label="Add a Wiki Page"
    factory = Page

#ADD LINK
from zopache.pages.page import Link
from zopache.pages.interfaces import ILink
from zopache.core.interfaces import ITreeSecurity

@view_component
@name('addLink')
@target(IView)
@context(IPage)
@implementer(ITreeSecurity)
class AddLink(AddByURLForm):
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
    


    
