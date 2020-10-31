from zopache.core.viewdecorators import *
from zopache.pages.interfaces import IPage

from zopache.business.addcompany import (
                                         AddOrganization,
                                         AddOnlineOrganization,
                                         AddNews)
from zopache.business.editpolitician import AddCandidate
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
class AddCMSNews(Base,AddNews):
    pass


@view_component
@name('iframe-addOnlineOrganization')
@target(IView)
@context(IPage)    
class AddCMSOnlineOrganziatin(Base,AddOnlineOrganization):
    pass
    
from dolmen.forms.base import interfaces
@view_component
@name('iframe-addPolitician')
@target(IView)
@context(IPage)    
class AddCMSPolitician(Base,AddCandidate):
    pass



@view_component
@name('iframe-addOnlineEvent')
@target(IView)
@context(IPage)
class AddCMSOnlineEvent(Base,AddOnlineEvent):
    pass

#ADD AN EVENT
@view_component
@name('iframe-addEvent')
@target(IView)
@context(IPage)
class AddCMSEvent(Base,AddEvent):
    pass
    
