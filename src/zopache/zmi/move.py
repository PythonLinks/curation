#This software is subject to the CV License Agreement.
from zope.interface import Interface
from zope.interface import implementer

from zopache.core.interfaces import ITreeSecurity
from cromlech.browser.exceptions import HTTPTemporaryRedirect
from zopache.core.viewdecorators import *
from zopache.core.baseform import Form

@view_component
@name('moveUp')
@context(Interface)
@implementer(ITreeSecurity)
class MoveUp(Form):
    
    def update(self):
        item = self.context
        parent = item.__parent__
        order = parent._order
        position = order.index(item.__name__)
        if position > 0:
           previousPosition = position -1
           key = order[position]
           previousKey = order [previousPosition]
           order [position] =  previousKey
           order [previousPosition] = key
           parent.updateOrder(order)
        url = self.absoluteURL(parent) + "/manage"
        raise HTTPTemporaryRedirect(url)
        
@view_component
@name('moveDown')
@context(Interface)
@implementer(ITreeSecurity)
class MoveDown(Form):
          
    def update(self):
        item = self.context    
        parent = item.__parent__
        order = parent._order
        position = order.index(item.__name__)
        length = len(order)
        if position < length:
           nextPosition = position + 1
           key = order[position]
           nextKey = order [nextPosition]
           order [position] =  nextKey
           order [nextPosition] = key
           parent.updateOrder(order)
        url = self.absoluteURL(parent) + "/manage"
        raise HTTPTemporaryRedirect(url)
