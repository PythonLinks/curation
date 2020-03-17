from zope.interface import implementer

from cromlech.security import Unauthorized

from zopache.business.interfaces import IMeetup
from zopache.pages.page import Page
from zopache.business.subscribe import Member

@implementer (IMeetup)
class Meetup (Page):
    webClass = "Meetup"
    clientClass = "category"
    hidden = False
    
    def __init__(self):
        Member.__init__(self)
        Page.__init__(self)
        
    def getTitle(self):
         if self.hidden:
            return "Hidden"
         return self.title

    def getSpecialization(self):
           return self.specialization
    
    def canView(self,view):
         if (self.hidden and
             (not view.isAuthenticated())):
             raise Unauthorized 

        
