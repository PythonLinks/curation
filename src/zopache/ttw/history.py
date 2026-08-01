import arrow
from pprint import pprint as pp
from zope.interface import Interface
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
from DateTime import DateTime
from zopache.core.breadcrumbs import Breadcrumbs
from zopache.core.interfaces import ITreeSecurity


def getHistory(obj, first=0, last=20):
    '''return history records for *obj* between *first* and *last* (indexes).

    Each record is a dict with "speaking" keys (see 'IStorage.history'),
    plus 'time' (a 'DateTime') and 'obj' (the state of *obj* as of that
    revision).
    '''
    jar = obj._p_jar
    oid = obj._p_oid
    db = jar.db()
    history = db.history(oid, last)[first:]
    for d in history:
        d['time'] = DateTime(d['time'])
        d['obj'] = db.open(at=d['tid']).get(oid)
    return history
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
                #Strange how the following line quite working. 
                #result = arrow.get(aTime)
                result = arrow.get(aTime.timeTime())                
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
           #Edit unindexes item, then indexes them.
           #Simpler o just not do either. 
           #if hasattr(contextParent,'postProcess'):
           #          contextParent.postProcess(view=self)
           newURL=self.absoluteURL(self.context.__parent__)+'/history'
           raise HTTPFound(newURL)






