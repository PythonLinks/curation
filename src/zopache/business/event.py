from zopache.pages.page import Page
from zopache.business.interfaces import IEvent
from zope.interface import implementer
from zopache.business.geocoding import GeoCode

@implementer (IEvent)
class Event (GeoCode,Page):
    webClass = "Company"
    clientClass = "Category"
    def postAddProcess(self,view):
        Address.postAddProcess(self.new)
        Page.postAddProcess(self.new)
