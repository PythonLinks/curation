from zopache.core.viewdecorators import *
from zopache.business.interfaces import IMeetup, IOnlineEvent
from zopache.business.meetup import Meetup
from zopache.business.onlineevent import OnlineEvent
from zopache.pages.interfaces import IPage
from zopache.business.addcompany import AddBase

@view_component
@name('addMeetup')
@target(IView)
@context(IPage)
class AddPage(AddBase):
    interface = IMeetup
    title="Add a Meetup"
    factory = Meetup

@view_component
@name('addOnlineEvent')
@target(IView)
@context(IMeetup)
class AddPage(AddBase):
    interface = IOnlineEvent
    title="Add an Online Event"
    factory = OnlineEvent
    
    


    
