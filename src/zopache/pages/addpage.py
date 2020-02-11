
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

class AddPageBase(AddCkHTMLBase,AddByTitleForm,UniqueName,Notify):
    def getSubTitle(self):
        return (
                "To a " +  
                self.context.webClass +
                u' called: ' +
                self.context.getTitle()
               )

    @property
    def actions(self):
        return Actions(
              AddAndView("Add and View", self.factory),
              AddAndCkEdit("Add and ckEdit", self.factory),
              AddAndAceEdit("Add and AceEdit", self.factory),
              formactions.Cancel("Cancel","Cancel"))
    
    def postAddProcess(self,view = None):
        Page.postAddProcess (self,view = self)
        self.notifyAdminsNewPage()
        
@view_component
@name('addPage')
@title("Add Page")
@target(IView)
@permissions('AddContent')
@context(IPage)    
class AddPage(AddPageBase):
    interface = IPage
    label="Add a Wiki Page"
    factory = Page
    

#ADD NEWS
@view_component
@name('addNews')
@title("Add News")
@target(IView)
@permissions('AddContent')
@context(IPage)    
class AddNews(AddPageBase):
    interface = INews
    label="Add a News Item"
    factory = News    

#LOCAION
@view_component
@name('addLocation')
@title("Add Location")
@target(IView)
@permissions('AddContent')
@context(IMap)    
class AddLocation(AddPageBase):
    interface = ILocation
    label="Add a Location"
    subTitle = 'Add a point on a map'
    factory = Location

#MAP
@view_component
@name('addSimpleMap')
@title("Add Map")
@target(IView)
@permissions('AddContent')
@context(IPage)    
class AddMap(AddPageBase):
    subTitle = 'Add a map'
    interface = IMap
    label="Add a Map"
    factory = Map
    


    
