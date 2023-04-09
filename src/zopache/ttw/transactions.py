import arrow
import time
import sys
import urllib
from pprint import pprint as pp

import transaction
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
from dm.historical import getHistory
from cromlech.security import permissions
from zopache.core.getroot import getZodbRoot


@view_component
@name('undo')
@title("Undo")
@permissions('Manage')
@context(Interface)
class Transactions(Page):
       label=''
       subTitle='Transactions'

       def results(self):
           root = getZodbRoot(self.context)
           db = root._p_jar.db()
           results = db.undoLog(0, 200)
           #results =  list(log) [:200]

           return results

       def pp(self,item):
           return pp(item)

       def reverseURL(self,id):
           url = self.url(self.context)
           id  = id.decode('utf-8')
           urlId = urllib.parse.quote_plus(id)
           url += '/reverse?id=' + urlId
           link  = self.href(url, id)
           return link
    
       template = tal_template('transactions.pt')
       def humanizeTime(self,aTime):
              now = time.time()
              t = int(now - aTime)
              #1 min = 60#1 min =
              #1 hour = 60 * 60 = 3600
              #1 day = 60 * 60 * 24 = 86400
         
              days= t//86400
              hours= (t-(days*86400))//3600
              minutes= (t - ((days*86400) + (hours*3600)))//60
              seconds= t - ((days*86400) + (hours*3600) + (minutes*60))
              result = (str(days) + 'd&nbsp;' +
                        str(hours) +'h&nbsp;' +
                        str (minutes) + 'm&nbsp;'+
                        str(seconds) +'s ')
              return result 


@view_component
@name('reverse')
@permissions('Manage')
@context(Interface)
class Restore(Page):
    def update(self):
           root = getZodbRoot(self.context)
           db = root._p_jar.db()
           id =  self.request.form ['id']
           self.id = id
           note = "Undid Transaction " + id
           transaction.get().note(note)           
           id  = id.encode('utf-8')
           db.undo (id)

    def render(self):
         return ('Transaction ' + self.id + '  was reversed')    

  










  
