from zopache.crud.addbytitleactions import *
from zopache.core.viewdecorators import *

from zopache.business.interfaces import (IMap,
                                         IMapBase,
                                         ICompany,
                                         ICity)
from zopache.business.imaporganization import IMapOrganization
from zopache.business.company import MapOrganization

from zopache.business.company import Company
from zopache.business.map import Map
from zopache.pages.addpage import AddAuthorizedPage, AddPage
from zopache.pages.addanonymous import AddAnonymousPage
from zopache.pages.interfaces import IPage,IPageBase
from zopache.business.exists import Duplicate
from zopache.business.geocoding import GeoCodeForm
from zopache.core.interfaces import ITreeSecurity
from zopache.business.map import City


class AddAll(AddAnonymousPage,GeoCodeForm):
    def update(self):
        AddPage.update(self)
        GeoCodeForm.update(self) 

@view_component
@name('addCompany')
@target(IView)
@context(IPageBase)    
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
@context(IPageBase)    
class AddRegion(AddAll):
    interface = IRegion
    factory = Region
    title = "Add a Region"

    

from zopache.business.socialnode import SocialNode
from zopache.business.iphonetree import ISocialNode
@view_component
@name('addSocialNode')
@target(IView)
@context(IPageBase)    
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
@name('addCompanyMap')
@target(IView)
@permissions('Manage')
@context(IPageBase)    
class AddMap(AddAuthorizedPage):
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
