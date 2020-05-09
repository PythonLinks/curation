
from BTrees.OOBTree import OOBTree
from zopache.pages.page import Page
from zopache.business.interfaces import IOnlineEvent
from zope.interface import implementer
from zopache.pages.page import Page
from zopache.business.subscribe import Member


#MAYBE JUST USED IN TEXAS GREENS
@implementer (IOnlineEvent)
class OnlineEvent (Page,Member):
    count = 0
    webClass = "OnlineEvent"
    clientClass = "Category"

    def __init__(self):
        Page.__init__(self)
        Member.__init__(self)
        
    def canView(self,view):
        pass
