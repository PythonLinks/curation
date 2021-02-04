
from BTrees.OOBTree import OOBTree
from zopache.pages.page import Page
from zopache.business.interfaces import IOnlineEvent
from zope.interface import implementer
from zopache.pages.page import Page
from zopache.business.subscribe import HasMembers


#MAYBE JUST USED IN TEXAS GREENS
@implementer (IOnlineEvent)
class OnlineEvent (Page,HasMembers):
    count = 0
    webClass = "OnlineEvent"
    clientClass = "Category"

    def __init__(self):
        Page.__init__(self)
        HasMembers.__init__(self)
        
    def canView(self,view):
        pass
