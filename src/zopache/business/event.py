
from BTrees.OOBTree import OOBTree
from zopache.pages.page import Page
from zopache.business.interfaces import IEvent
from zope.interface import implementer
from zopache.business.geocoding import GeoCodeObject
from zopache.pages.page import Page
from zopache.business.subscribe import Member
from zopache.business.subscribe import Member

@implementer (IEvent)
class Event (GeoCodeObject,Page,Member):
    count = 0
    webClass = "Event"
    clientClass = "Category"

    def __init__(self):
        Page.__init__(self)
        GeoCodeObject.__init__(self)
        Member.__init__(self)


    def postAddProcess(self,view):
        GeoCode.postAddProcess(self, view = view)
        Page.postAddProcess(self, view = view)
        
    def canView(self,view):
        pass
