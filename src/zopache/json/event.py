

from zope.interface import implementer
# -*- coding: utf-8 -*-

from BTrees.OOBTree import OOBTree

from zopache.json.interfaces import IJSONEvent
from zopache.json.markdown import JSONMarkdown
from zopache.business.member import Member

class MembersBase(object):

    def isMemberA(self,view,attribute):
         principal = view.request.principal
         if principal == anonymous:
            return False
         principalId = principal.__name__
         theMember = self.getOneMember(principalId)
         return getattr(theMember,attribute,False)
     
    def getOneMember(self,name):
        members = self.members
        if name in members:
           theMember = members[name] 
           if theMember.__class__ == Member:
               return theMember
        else:
              theMember = Member (name)   
              members [name] = theMember
              return theMember
    
    def isMember(self,view):
        if not view.isAuthenticated():
           return False
        if not hasattr(self,'members'):
           return False
        members = self.members
        name = view.request.principal.__name__
        if name in members:
            return True
        return False


@implementer(IJSONEvent)
class JSONEvent(JSONMarkdown, MembersBase):
    webClass   = 'JSONEvent'

    def __init__ (self):
        JSONMarkdown.__init__(self)
        self._members =  OOBTree()

    def getMembers(self):
         return self._members
     
    members = property(getMembers) 
    
