from dolmen.forms.base import Actions

from zopache.pages.pageactions import *
from zopache.crud import actions as formactions
from zopache.pages.pageactions import *
from zopache.core.viewdecorators import *
from zopache.ttw.html import CkScripts
from zopache.ttw.html import AddCkHTMLBase

from zopache.core.uniquename import UniqueName
from zopache.crud.forms import AddByTitleForm
from zopache.business.interfaces import IMap, ICompany,IMapOrganization
from zopache.business.interfaces import ICompanyOrOrganization
from zopache.business.interfaces import IOrganization, IOnlineOrganization
from zopache.business.company import MapOrganization

from zopache.business.interfaces import  IOnlineEvent, IEvent
from zopache.business.company import Company, Organization, OnlineOrganization
from zopache.business.map import Map
from zopache.pages.addpage import AddPageBase
from zopache.pages.interfaces import IPage
from zopache.business.exists import Duplicate
from zopache.business.geocoding import GeoCodeForm
from zopache.business.politician import IPolitician, Politician
from zopache.pages.interfaces import  INews
from zopache.pages.page import  News
from zopache.pages.addpage import AddPageBase
from zopache.pages.addanonymous import AddAnonymous


#ADD NEWS
@view_component
@name('addNews')
@target(IView)
@context(IPage)
class AddNews(AddPageBase):
    interface = INews
    title = "Add a News Item"
    subtitle = "Because the MSM does not cover it."
    factory = News
    
@view_component
@name('addCompany')
@target(IView)
@context(IPage)    
class AddCompany(AddPageBase,GeoCodeForm):
    interface = ICompany
    label="Add a Company"
    factory = Company
    title = "Add a Company"
    def update(self):
        AddPageBase.update(self)
        GeoCodeForm.update(self) 
    
@view_component
@name('addOrganization')
@title("Add Organization")
@target(IView)
@context(IPage)    
class AddOrganization(AddAnonymous,GeoCodeForm):
    interface = IOrganization
    factory = Organization
    title = "Add an Organization"



    
@view_component
@name('addOnlineOrganization')
@title("Add Online Organization")
@target(IView)
@context(IPage)    
class AddOnlineOrganization(AddAnonymous,GeoCodeForm):
    interface = IOnlineOrganization
    factory = OnlineOrganization
    title = "Add an Online Organization"
        
from dolmen.forms.base import interfaces
@view_component
@name('addPolitician')
@target(IView)
@context(IPage)    
class AddPolitician(AddAnonymous,GeoCodeForm):
    interface = IPolitician
    factory = Politician
    title = "Add a Politician"
    def update(self):
        AddAnonymous.update(self)
        GeoCodeForm.update(self) 
    """
    def updateWidgets(self):
        ddBase.update(self)
        #item =self.fields['endorsedBy']
        it =object.__setattr__(item,'mode','multiselect')
        super().updateWidgets()
     """   

from zopache.business.driver import IAddDriver, Driver    
@view_component
@name('addDriver')
@target(IView)
@context(IPage)    
class AddDriver(AddAnonymous,GeoCodeForm):
    interface = IAddDriver
    factory = Driver
    title = "Offer to be a driver."

    def update(self):
        AddAnonymous.update(self)
        GeocodeForm.update(self) 
              
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


@view_component
@name('addMapOrganization')
@target(IView)
@permissions('AddContent')
@context(IPage)    
class AddMapOrganization(AddPageBase):
    subTitle = ''
    interface = IMapOrganization
    label="Add a Map Organizatin"
    factory = MapOrganization    
    
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
