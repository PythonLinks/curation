from zopache.pages.page import Page
from zopache.business.interfaces import IEvent
from zope.interface import implementer
from zopache.business.geocoding import GeoCode
from zopache.pages.page import Page

@implementer (IEvent)
class Event (GeoCode,Page):
    count = 0
    webClass = "Event"
    clientClass = "Category"
    def postAddProcess(self,view):
        GeoCode.postAddProcess(self, view = view)
        Page.postAddProcess(self, view = view)
        
    def canView(self,view):
        pass
