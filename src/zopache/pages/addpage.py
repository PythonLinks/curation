
from dolmen.forms.base import Actions
from zopache.pages.pageactions import *
from zopache.crud import actions as formactions
from zopache.pages.pageactions import *
from zopache.core.viewdecorators import *
from zopache.ttw.html import CkScripts
from zopache.ttw.html import AddCkHTMLBase

from zopache.core.uniquename import UniqueName
from zopache.crud.forms import AddByTitleForm
from zopache.pages.interfaces import IMap, ILocation, INews, IPage
from zopache.pages.page import Page, News
from zopache.pages import Map, Location
from zopache.ttw.mail import Notify
from zopache.core.interfaces import ITreeSecurity

class AddPageBase(AddCkHTMLBase,AddByTitleForm,UniqueName,Notify):
    def getSubTitle(self):
        
        return (
                "To a " +  
                self.context.webClass +
                u' called: ' +
                self.context.getTitle()
               )
    actions = Actions()
    def update(self):
        if self.treeSecurity():
            self.setActions()
            
    def setActions(self):       
        self.actions = Actions(
              AddAndView("Add and View", self.factory),
              AddAndCkEdit("Add and ckEdit", self.factory),
              AddAndAceEdit("Add and AceEdit", self.factory),
              formactions.Cancel("Cancel","Cancel"))
    
    def postAddProcess(self,view = None):
        self.new.postAddProcess (view = self)
        self.notifyAdminsNewPage()
        
@view_component
@name('addPage')
@target(IView)
@context(IPage)
@implementer(ITreeSecurity)
class AddPage(AddPageBase):
    interface = IPage
    label="Add a Wiki Page"
    factory = Page

#ADD LINK
from zopache.pages.page import Link
from zopache.pages.interfaces import ILink
@view_component
@name('addLink')
@target(IView)
@context(IPage)
class AddLink(AddPageBase):
    interface = ILink
    title = "Add a Link"
    subtitle = "To a remote web page."
    factory = Link
    
#ADD NEWS
@view_component
@name('addNews')
@target(IView)
@context(IPage)
class AddNews(AddPageBase):
    interface = INews


#LOCAION
@view_component
@name('addLocation')
@target(IView)
@context(IMap)
@implementer(ITreeSecurity)
class AddLocation(AddPageBase):
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
class AddMap(AddPageBase):
    subTitle = 'Add a map'
    interface = IMap
    label="Add a Map"
    factory = Map
    


    
