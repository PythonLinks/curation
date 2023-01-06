import time
from zope.interface import Interface
from zope import schema
from slugify import slugify
from html import unescape

from BTrees.OOBTree import OOBTree
from dolmen.forms.base.markers import FAILURE, SUCCESS

from zopache.pages.page import Page
from zopache.core.viewdecorators import *
from zopache.pages.interfaces import IPage
from zopache.crud.interfaces import IContainer
from zopache.core.uniquename import UniqueName


from bs4 import BeautifulSoup
from zopache.remote.rssdownload import fetchAll
from zopache.crud.getimage import getImage
from zopache.remote.mastodon.article import TootedArticle
from zopache.remote.mastodon.interfaces import IMastodonAccount

@implementer (IMastodonAccount)
class MastodonAccount(Page,UniqueName):
    webClass = "RemoteAccount"
    htmlSummary = True
    title = ""
    twitterId = ''
    mastodonId = ''
    keepAllArticles = False
    crawledToStart = False
    minId = None 
    maxId = None
    
    def __delitem__(self,key):
        siteRoot = self.getPublicationRoot()
        item = self[key]
        siteRoot.unIndexItem(item)
        BTreeContainer.__delitem__(self,key)
        
    def __setitem__(self,  key,item):
        BTreeContainer.__setitem__(self,key,item)
        siteRoot = self.getPublicationRoot()     
        siteRoot.addItem(item)
        
    @property
    def remoteURL(self):
        blank,user, server = self.parts()
        return 'https://' + server + '/@' + user

    def parts(self):
        return self.mastodonId.split('@')
    
    def reset(self):
         self.upUntil = time.time()
         self.backTo = self.upUntil
    
    def __init__(self):
         self.localArticles = OOBTree()
         self.reset()
         Page.__init__(self)
        
    def postAddProcess(self,view = None):
        Page.postAddProcess(self,view = view)
        if self.logoURL:
            getImage(self,self.logoURL)
        self.fetchArticles([self],view)

    #COPY OF THIS HERE AND IN RSS.PY    
    def fetchArticles(self,feeds,view):    
        result = fetchAll(feeds,view)
        for item in result:
            if item[0] ==  FAILURE:  
               view.submissionErrors.append( "ERROR:" + str(item [1:]))
        self.status='RSS Feeds were downloaded.'
        

    async def processResponse(self, session, response,view):
          html  =  await response.text()
          feed = feedparser.parse(html)
          entries = feed['entries']
          await self.createArticles(entries,view)

          

import crom
from zopache.zmi.interfaces import IURLSegment
@crom.adapter
@crom.sources(IMastodonAccount)
@crom.target(IURLSegment)
class IMastodonAccountAdaptor(object):
    def __init__(self,context):
        self.context=context   

    def getSegment(self):
        return 'manage'

