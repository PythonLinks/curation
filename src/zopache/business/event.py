
from BTrees.OOBTree import OOBTree
from zopache.pages.page import Page
from zopache.business.interfaces import IEvent,IOnlineEvent
from zope.interface import implementer
from zopache.business.geocoding import GeoCodeObject
from zopache.pages.page import Page
from zopache.business.subscribe import Member

@implementer (IOnlineEvent)
class OnlineEvent (Page,Member):
    count = 0
    webClass = "Event"
    clientClass = "Category"
    webApproved = False
    
    def __init__(self):
        Page.__init__(self)
        Member.__init__(self)

    def postAddProcess(self,view):
        Page.postAddProcess(self, view = view)
        
    def canView(self,view):
        return True

@implementer(IEvent)
class Event(OnlineEvent,GeoCodeObject):
    def __init__(self):
        Page.__init__(self)
        GeoCodeObject.__init__(self)
        Member.__init__(self)
