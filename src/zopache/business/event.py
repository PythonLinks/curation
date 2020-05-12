
from BTrees.OOBTree import OOBTree
from zopache.pages.page import Page
from zopache.business.interfaces import IEvent,IOnlineEvent
from zope.interface import implementer
from zopache.business.geocoding import GeoCodeObject
from zopache.pages.page import Page
from zopache.business.subscribe import Member

class EventBase(Page,Member):
    count = 0
    webClass = "Event"
    clientClass = "Category"
    webApproved = False
    
    def __init__(self):
        Page.__init__(self)
        Member.__init__(self)

    def postAddProcess(self,view=None):
        if view.treeSecurity():
           self.webApproved = True
        Page.postAddProcess(self,view)
        
    def canView(self,view):
        return True

@implementer (IOnlineEvent)
class OnlineEvent (EventBase):
    webClass = "OnlineEvent"    

from zopache.pages.location import LocationLeaf
@implementer(IEvent)
class Event(EventBase,GeoCodeObject,LocationLeaf):
    def __init__(self):
        Page.__init__(self)
        GeoCodeObject.__init__(self)
        Member.__init__(self)
