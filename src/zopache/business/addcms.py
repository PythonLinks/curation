from dolmen.forms.base import Actions

from zopache.pages.pageactions import *
from zopache.crud import actions as formactions
from zopache.pages.pageactions import *
from zopache.core.viewdecorators import *
from zopache.ttw.html import CkScripts
from zopache.ttw.html import AddCkHTMLBase

from zopache.core.uniquename import UniqueName
from zopache.crud.forms import AddByTitleForm
from zopache.business.interfaces import IMap, ICompany
from zopache.business.interfaces import ICompanyOrOrganization
from zopache.business.interfaces import IOrganization, IOnlineOrganization

from zopache.business.interfaces import  IOnlineEvent, IEvent
from zopache.business.company import Company, Organization, OnlineOrganization
from zopache.business.map import Map
from zopache.pages.addpage import AddPageBase
from zopache.pages.interfaces import IPage
from zopache.business.exists import Duplicate
from zopache.business.geocoding import GeoCodeForm
from zopache.business.politician import IPolitician, Politician

from zopache.business.addcompany import AddBase as AddCompanyBase
from dolmen.view import  make_view_response

from zopache.business.addcompany import (AddPolitician,
                                         AddOrganization,
                                         AddOnlineOrganization)

from zopache.business.addmeetup import AddEvent, AddOnlineEvent

class Base(object):
     def getNavBar(self):
         return ""
     
@view_component
@name('iframe-addOrganization')
@target(IView)
@context(IPage)    
class AddCMSOrganization(Base,AddOrganization):
    pass

@view_component
@name('iframe-addNews')
@target(IView)
@context(IPage)    
class AddCMSNews(Base,AddOrganization):
    pass

from zopache.pages.addpage import AddNews
@view_component
@name('iframe-addOnlineOrganization')
@target(IView)
@context(IPage)    
class AddNews(Base,AddNews):
    pass
    
from dolmen.forms.base import interfaces
@view_component
@name('iframe-addPolitician')
@target(IView)
@context(IPage)    
class AddPolitician(Base,AddPolitician):
    pass



@view_component
@name('iframe-addOnlineEvent')
@target(IView)
@context(IPage)
class AddOnlineEvent(Base,AddOnlineEvent):
    pass

#ADD AN EVENT
@view_component
@name('iframe-addEvent')
@target(IView)
@context(IPage)
class AddEvent(Base,AddEvent):
    pass
    
