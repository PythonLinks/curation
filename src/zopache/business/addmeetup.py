from zopache.core.viewdecorators import *
from zopache.business.interfaces import IMeetup, IOnlineEvent, IEvent
from zopache.business.meetup import Meetup
from zopache.business.event import Event, OnlineEvent
from zopache.pages.interfaces import IPage
from zopache.business.geocoding import GeoCodeForm
from zopache.pages.addanonymous import AddAnonymousPage

@view_component
@name('addMeetup')
@target(IView)
@context(IPage)
class AddMeetup(AddAnonymousPage):
    interface = IMeetup
    title="Add a Meetup Group"
    factory = Meetup

@view_component
@name('addOnlineEvent')
@target(IView)
@context(IPage)
class AddOnlineEvent(AddAnonymousPage):
    interface = IOnlineEvent
    title="Add an Online Event"
    factory = OnlineEvent

#ADD AN EVENT
@view_component
@name('addEvent')
@target(IView)
@context(IPage)
class AddEvent(AddAnonymousPage):
    interface = IEvent
    factory = Event
    title = "Add a Real World Event"
    def update(self):
        AddAnonymous.update(self)
        GeoCodeForm.update(self)     
    


    
