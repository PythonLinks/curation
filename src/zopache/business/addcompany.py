from zopache.crud.addbytitleactions import *
from zopache.core.viewdecorators import *
from zopache.ttw.htmlviews import CkScripts
from zopache.ttw.htmlviews import AddCkHTMLBase

from zopache.core.uniquename import UniqueName
from zopache.crud.addbyurl import  AddByURLForm
from zopache.crud.forms import AddByTitleForm
from zopache.business.interfaces import (IMap,
                                         IMapBase,
                                         ICompany,
                                         ICity)
from zopache.business.imaporganization import IMapOrganization
from zopache.business.company import MapOrganization

from zopache.business.interfaces import  IOnlineEvent, IEvent
from zopache.business.company import Company
from zopache.business.map import Map
from zopache.pages.addpage import AddAuthorizedPage, AddPage
from zopache.pages.addanonymous import AddAnonymousPage
from zopache.pages.interfaces import IPage
from zopache.business.exists import Duplicate
from zopache.business.geocoding import GeoCodeForm
from zopache.pages.interfaces import  INews
from zopache.pages.page import  News
from zopache.core.interfaces import ITreeSecurity
from zopache.business.driver import IAddDriver, Driver
from zopache.business.map import City

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

class AddAll(AddAnonymousPage,GeoCodeForm):
    def update(self):
        AddPage.update(self)
        GeoCodeForm.update(self) 

@view_component
@name('addCompany')
@target(IView)
@context(IPage)    
class AddCompany(AddAll):
    interface = ICompany
    label="Add a Company"
    factory = Company
    title = "Add a Company"

from zopache.business.interfaces import IRegion
from zopache.business.region import Region
@view_component
@name('addRegion')
@target(IView)
@context(IPage)    
class AddRegion(AddAll):
    interface = IRegion
    factory = Region
    title = "Add a Region"

    

from zopache.business.socialnode import SocialNode
from zopache.business.iphonetree import ISocialNode
@view_component
@name('addSocialNode')
@target(IView)
@context(IPage)    
class AddPhoneTree(AddAll):
    interface = ISocialNode
    factory = SocialNode
    title = "Add a Social Node"    

#CITY    
@view_component
@name('addCity')
@target(IView)
@context(IMapBase)
@implementer(ITreeSecurity)
class AddCity(AddAuthorizedPage, GeoCodeForm):
    interface = ICity
    label="Add a City"
    subTitle = 'Add a city to a map'
    factory = City
    preamble = "If two map pins are too close together, they overlap.  The "
    preamble += "user can only see one pin, they can only click on one pin. "
    preamble += 'The solution to this problem is to add a "City" object. '
    preamble += 'And then cut the overlapping pins from the map using the'
    preamble += 'Manage->Manage manu, past them into the city object. '
    preamble += 'The city title can then be "San Jose (2 items)" '
    preamble += 'Or even "San Jose / Santa Clara (two items)" '
    preamble += 'Check out San Jose in California for an example. '
    def update(self):
        AddAuthorizedPage.update(self)
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
@name('addCompanyMap')
@target(IView)
@permissions('Manage')
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
