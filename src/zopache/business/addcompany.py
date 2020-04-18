from dolmen.forms.base import Actions

from zopache.pages.pageactions import *
from zopache.crud import actions as formactions
from zopache.pages.pageactions import *
from zopache.core.viewdecorators import *
from zopache.ttw.html import CkScripts
from zopache.ttw.html import AddCkHTMLBase

from zopache.core.uniquename import UniqueName
from zopache.crud.forms import AddByTitleForm
from zopache.business.interfaces import IMap, IAddCompany, IAddOrganization
from zopache.business.interfaces import ICompanyOrOrganization, IEvent

from zopache.business.company import Company, Organization
from zopache.business.map import Map
from zopache.pages.addpage import AddPageBase
from zopache.pages.interfaces import IPage
from zopache.core.interfaces import ITreeSecurity
from zopache.business.event import Event
from zopache.business.exists import DuplicateOrganization
from zopache.business.geocoding import GeoCodeForm
from zopache.business.politician import IAddPolitician, Politician
from zopache.business.tree import IAddTree, Tree

class AddBase(AddPageBase):
    count = 0 
    layoutName = "UserMenu"
    subTitle = "All submissions are reviewed before becoming being publicly visible."
    
    @property
    def actions(self):
        return Actions(
              AddAndView("Add and View", self.factory),
              formactions.Cancel("Cancel","Cancel"))
    
@view_component
@name('addCompany')
@target(IView)
@context(IPage)    
class AddCompany(GeoCodeForm,AddBase):
    interface = IAddCompany
    label="Add a Company"
    factory = Company
    title = "Add a Company"

    
@view_component
@name('addOrganization')
@title("Add Organization")
@target(IView)
@context(IPage)    
class AddOrganization(GeoCodeForm,AddBase):
    interface = IAddOrganization
    factory = Organization
    title = "Add an Organization"
    subTitle = "All submissions are reviewed before becoming publicly visible."
    dataValidators = [DuplicateOrganization]
    
from dolmen.forms.base import interfaces
@view_component
@name('addPolitician')
@target(IView)
@context(IPage)    
class AddPolitician(AddBase):
    interface = IAddPolitician
    factory = Politician
    title = "Add a Politician"
    subTitle = "All submissions are reviewed before becoming publicly visible."
    dataValidators = [DuplicateOrganization]    
    def updateWidgets(self):
        item =self.fields['endorsedBy']
        it =object.__setattr__(item,'mode','multiselect')
        super().updateWidgets()
    
@view_component
@name('addTree')
@target(IView)
@context(IPage)    
class AddTree(AddBase):
    interface = IAddTree
    factory = Tree
    title = "Add a Tree"
    subTitle = "All submissions are reviewed before becoming publicly visible."
    dataValidators = [DuplicateOrganization]

from zopache.business.driver import IAddDriver, Driver    
@view_component
@name('addDriver')
@target(IView)
@context(IPage)    
class AddDriver(AddBase):
    interface = IAddDriver
    factory = Driver
    title = "Offer to be a driver."
    subTitle = "All submissions are reviewed before becoming publicly visible."
    dataValidators = [DuplicateOrganization]    


#ADD AN EVENT
@view_component
@name('addEvent')
@target(IView)
@context(IPage)
@implementer (ITreeSecurity)
class AddEvemt(AddBase):
    interface = IEvent
    factory = Event
    title = "Add an Event"
    subTitle = ""

    @property
    def actions(self):
        return Actions(
              AddAndView("Add and View", self.factory),
              formactions.Cancel("Cancel","Cancel"))
            
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
