from zopache.core.viewdecorators import *
from zopache.business.interfaces import IMeetup, IOnlineEvent, IEvent
from zopache.business.meetup import Meetup
from zopache.business.event import Event, OnlineEvent
from zopache.pages.interfaces import IPage
from zopache.pages.addpage import AddPageBase

#Next line should disappear
from zopache.pages.addpage import AddPageBase as AddBase

from zopache.business.geocoding import GeoCodeForm
from zopache.pages.addanonymous import AddAnonymous

@view_component
@name('addMeetup')
@target(IView)
@context(IPage)
class AddMeetup(AddPageBase):
    interface = IMeetup
    title="Add a Meetup Group"
    factory = Meetup

@view_component
@name('addOnlineEvent')
@target(IView)
@context(IPage)
class AddOnlineEvent(AddAnonymous):
    interface = IOnlineEvent
    title="Add an Online Event"
    factory = OnlineEvent

#ADD AN EVENT
@view_component
@name('addEvent')
@target(IView)
@context(IPage)
class AddEvent(AddAnonymous):
    interface = IEvent
    factory = Event
    title = "Add a Real World Event"
    def update(self):
        AddAnonymous.update(self)
        GeoCodeForm.update(self)     
    


    
