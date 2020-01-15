import arrow
from zope.interface import Interface
from pprint import pprint as pp 
from .css import ICSS
from .javascript import IJavascript
from .interfaces import ISource, IHTML
from . import tal_template
from zopache.core.page  import  Page
from dolmen.view import name, context, view_component
from cromlech.browser.directives import title
from crom import target, order
from zope.interface import implementer
from zopache.ttw.interfaces import IHistoricDetails
from cromlech import browser
from cromlech.browser.exceptions import HTTPFound
from zopache.ttw.interfaces import IHistoryItem
from dm.historical import getHistory
from zopache.core.breadcrumbs import Breadcrumbs
from zopache.core.interfaces import ITreeSecurity

"""
#Maybe this is a much simpler versin for more recent zodb. 
def getHistory(item, size=40):
         db=item._p_jar.db()
         oid=item.__data._p_oid
         for version in db.history(oid,size):
             tid=version['tid']   #tid=the Transaction ID
             historicConnection= Connection(db,before=tid)
             historicObject=historicConnection.get(oid)
             yield historicObject
"""
@view_component
@name('history')
@context(ISource)
@implementer(ITreeSecurity)
class History(Page, Breadcrumbs):
       label=''
       subTitle='Historic Versions'
           
       def results(self):
           return getHistory(self.context,last=200)

       def pp(self,item):
           return pp(item)
    
       template = tal_template('history.pt')
       def humanizeTime(self,aTime):
                result = arrow.get(aTime)
                result = result.humanize()
                if (result [-3:] == 'ago'):
                   result = result [:-3]
                return result
         
@view_component
@name('historicindex')
@title("Historic Index")
@context(IHistoryItem)
@implementer (IHistoricDetails)
class HistoricIndex(Page):
       def render(self ):
           before = '<html><body></body><textarea rows="20" cols="80" margin: 20px; padding: 20px;>'
           content = self.context.item['obj'].source
           after = "</textarea></body></html>"
           return  before + content + after


@view_component
@name('historicview')
@title("Historic View")
@context(IHistoryItem)
@implementer (IHistoricDetails)
class HistoricView (Page):
       def render(self ):
           item=self.context.item['obj']           
           return item(self)

@view_component
@name('restore')
@context(IHistoryItem)
@implementer (IHistoricDetails)
class Restore(Page):
       def render(self ):
           context=self.context
           contextParent=context.__parent__
           item=context.item['obj']
           if hasattr(item,'title'):
              contextParent.title=item.title
           if hasattr(item,'source'):
              contextParent.source=item.source
           if hasattr(contextParent,'postProcess'):
                     contextParent.postProcess(view=self)
           newURL=self.url(self.context.__parent__)+'/history'
           raise HTTPFound(newURL)






