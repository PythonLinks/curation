from zopache.core.viewdecorators import *
from zopache.business.interfaces import IMeetup, IOnlineEvent, IEvent
from zopache.business.meetup import Meetup
from zopache.business.onlineevent import OnlineEvent
from zopache.business.event import Event
from zopache.pages.interfaces import IPage
from zopache.business.addcompany import AddBase
from zopache.business.geocoding import GeoCodeForm

@view_component
@name('addMeetup')
@target(IView)
@context(IPage)
class AddMeetup(AddBase):
    interface = IMeetup
    title="Add a Meetup Group"
    factory = Meetup

@view_component
@name('addOnlineEvent')
@target(IView)
@context(IPage)
class AddOnlineEvent(AddBase):
    interface = IOnlineEvent
    title="Add an Online Event"
    factory = OnlineEvent

#ADD AN EVENT
@view_component
@name('addEvent')
@target(IView)
@context(IPage)
class AddEvent(AddBase):
    interface = IEvent
    factory = Event
    title = "Add an Online Event"
    def update(self):
        AddBase.update(self)
        GeocodeForm.update(self)     
    


    
