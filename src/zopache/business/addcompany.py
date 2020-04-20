from dolmen.forms.base import Actions

from zopache.pages.pageactions import *
from zopache.crud import actions as formactions
from zopache.pages.pageactions import *
from zopache.core.viewdecorators import *
from zopache.ttw.html import CkScripts
from zopache.ttw.html import AddCkHTMLBase

from zopache.core.uniquename import UniqueName
from zopache.crud.forms import AddByTitleForm
from zopache.business.interfaces import IMap, ICompany, ITree
from zopache.business.interfaces import ICompanyOrOrganization
from zopache.business.interfaces import IOrganization, IOnlineOrganization

from zopache.business.interfaces import  IOnlineEvent, IEvent
from zopache.business.company import Company, Organization, OnlineOrganization
from zopache.business.map import Map
from zopache.pages.addpage import AddPageBase
from zopache.pages.interfaces import IPage
from zopache.core.interfaces import ITreeSecurity
from zopache.business.event import Event,OnlineEvent
from zopache.business.exists import Duplicate
from zopache.business.geocoding import GeoCodeForm
from zopache.business.politician import IAddPolitician, Politician
from zopache.business.tree import Tree

class AddBase(AddPageBase):
    count = 0 
    layoutName = "UserMenu"
    subTitle = "All submissions are reviewed before becoming being publicly visible."
    allowAnonymous = True    
    dataValidators = [Duplicate]
    
    def update(self):
        AddPageBase.update(self)
        self.actions = Actions(
              AddAndView("Add and View", self.factory),
              formactions.Cancel("Cancel","Cancel"))
        
@view_component
@name('addCompany')
@target(IView)
@context(IPage)    
class AddCompany(GeoCodeForm,AddBase):
    interface = ICompany
    label="Add a Company"
    factory = Company
    title = "Add a Company"
    def update(self):
        AddBase.update(self)
        GeocodeForm.update(self) 
    
@view_component
@name('addOrganization')
@title("Add Organization")
@target(IView)
@context(IPage)    
class AddOrganization(GeoCodeForm,AddBase):
    interface = IOrganization
    factory = Organization
    title = "Add an Organization"

@view_component
@name('addOnlineOrganization')
@title("Add Online Organization")
@target(IView)
@context(IPage)    
class AddOnlineOrganization(GeoCodeForm,AddBase):
    interface = IOnlineOrganization
    factory = OnlineOrganization
    title = "Add an Online Organization"



        
from dolmen.forms.base import interfaces
@view_component
@name('addPolitician')
@target(IView)
@context(IPage)    
class AddPolitician(GeoCodeForm,AddBase):
    interface = IAddPolitician
    factory = Politician
    title = "Add a Politician"
    def update(self):
        AddBase.update(self)
        GeocodeForm.update(self) 
    
    def updateWidgets(self):
        AddBase.update(self)
        item =self.fields['endorsedBy']
        it =object.__setattr__(item,'mode','multiselect')
        super().updateWidgets()

        
@view_component
@name('addTree')
@target(IView)
@context(IPage)    
class AddTree(AddBase):
    interface = ITree
    factory = Tree
    title = "Add a Tree"
    def update(self):
        AddBase.update(self)
        GeocodeForm.update(self) 

from zopache.business.driver import IAddDriver, Driver    
@view_component
@name('addDriver')
@target(IView)
@context(IPage)    
class AddDriver(AddBase):
    interface = IAddDriver
    factory = Driver
    title = "Offer to be a driver."
    def update(self):
        AddBase.update(self)
        GeocodeForm.update(self) 
  

#ADD AN EVENT
@view_component
@name('addEvent')
@target(IView)
@context(IPage)
@implementer (ITreeSecurity)
class AddEvemt(AddBase):
    interface = IOnlineEvent
    factory = OnlineEvent
    title = "Add an Online Event"
            
@view_component
@name('addCompanyMap')
@target(IView)
@permissions('AddContent')
@context(IPage)    
class AddMap(AddPageBase):
    subTitle = 'Add a map'
    interface = IMap
    label="Add a Map"
    factory = Map
    
import crom
from dolmen.forms.base.interfaces import IWidget
from dolmen.forms.ztk.widgets.collection import (
                      MultiSelectFieldWidget,CollectionSchemaField)
from dolmen.forms.ztk.widgets.choice import (
                               ChoiceSchemaField, ChoiceFieldWidget)
@crom.adapter
@crom.name('input')
@crom.target(IWidget)
@crom.sources(CollectionSchemaField, ChoiceSchemaField, Interface, Interface)
class DisplayWidget(MultiSelectFieldWidget):
      pass
