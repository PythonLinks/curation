from zopache.pages.pageactions import *
from zopache.core.viewdecorators import *
from zopache.ttw.htmlviews import CkScripts
from zopache.ttw.htmlviews import AddCkHTMLBase

from zopache.core.uniquename import UniqueName
from zopache.crud.addbyurl import  AddByURLForm
from zopache.crud.forms import AddByTitleForm
from zopache.business.interfaces import IMap, ICompany,IMapOrganization
from zopache.business.interfaces import ICompanyOrOrganization
from zopache.business.interfaces import IAddOrganization, IOnlineOrganization
from zopache.business.company import MapOrganization

from zopache.business.interfaces import  IOnlineEvent, IEvent
from zopache.business.company import Company, Organization, OnlineOrganization
from zopache.business.map import Map
from zopache.pages.addpage import AddAuthorizedPage
from zopache.pages.addanonymous import AddAnonymousPage
from zopache.pages.interfaces import IPage
from zopache.business.exists import Duplicate
from zopache.business.geocoding import GeoCodeForm
from zopache.business.politician import IAddPolitician, Politician
from zopache.pages.interfaces import  INews
from zopache.pages.page import  News
from zopache.core.interfaces import ITreeSecurity
from zopache.business.driver import IAddDriver, Driver

#ADD NEWS
@view_component
@name('addNews')
@target(IView)
@context(IPage)
class AddNews(AddAuthorizedPage):
    interface = INews
    emailApparoved = True
    title = "Add a News Item"
    subtitle = "Because the MSM does not cover it."
    factory = News
    
@view_component
@name('addCompany')
@target(IView)
@context(IPage)    
class AddCompany(AddAnonymousPage,GeoCodeForm):
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
class AddOrganization(AddAnonymousPage,GeoCodeForm):
    interface = IAddOrganization
    factory = Organization
    title = "Add an Organization"
    def update(self):
        AddAnonymousPage.update(self)
        GeoCodeForm.update(self)


@view_component
@name('addDriver')
@target(IView)
@context(IPage)    
class AddDriver(AddAnonymousPage,GeoCodeForm):
    interface = IAddDriver
    factory = Driver
    title = "Offer to be a driver."

    def update(self):
        AddAnonymousPage.update(self)
        GeocodeForm.update(self) 

@view_component
@name('addOrgByURL')
@target(IView)
@context(IPage)
@implementer(ITreeSecurity)
class AddOrganizationByURL(AddByURLForm):
    factory = Organization
    title = "Add an Organization by URL"

@view_component
@name('addOnlineOrganization')
@title("Add Online Organization")
@target(IView)
@context(IPage)    
class AddOnlineOrganization(AddAnonymousPage,GeoCodeForm):
    interface = IOnlineOrganization
    factory = OnlineOrganization
    title = "Add an Online Organization"
        


@view_component
@name('addPolitician')
@target(IView)
@context(IPage)    
class AddPolitician(AddAnonymousPage,GeoCodeForm):
    interface = IAddPolitician
    factory = Politician
    title = "Add a Politician"
    def update(self):
        AddAnonymousPage.update(self)
        GeoCodeForm.update(self)

    """
    def updateWidgets(self):
        ddBase.update(self)
        #item =self.fields['endorsedBy']
        it =object.__setattr__(item,'mode','multiselect')
        super().updateWidgets()
     """
    
@view_component
@name('addCompanyMap')
@target(IView)
@permissions('AddContent')
@context(IPage)    
class AddMap(AddAuthorizedPage):
    subTitle = 'Add a map'
    interface = IMap
    label="Add a Map"
    factory = Map


@view_component
@name('addMapOrganization')
@target(IView)
@context(IPage)
@implementer(ITreeSecurity)
class AddMapOrganization(AddAuthorizedPage):
    title = "Add an Organization with a Map"
    subTitle = 'Usually for state parties. '
    interface = IMapOrganization
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
