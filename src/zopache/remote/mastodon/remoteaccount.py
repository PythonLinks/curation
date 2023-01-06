import time

from dolmen.container import BTreeContainer
from BTrees.OOBTree import OOBTree

from zopache.core.viewdecorators import *
from zopache.core.uniquename import UniqueName
from zopache.pages.used import Used
from zopache.remote.mastodon.interfaces import IMastodonAccount
from zopache.core import Container
from zopache.ttw.html import UntrustedHTMLBase
from zopache.crud.getimage import getImage
from zopache.core.ancestors import Ancestors

#all imports are used

@implementer (IMastodonAccount)
class MastodonAccount(
                    Container,
                    Used,
                    UniqueName,
                    Ancestors,
                    UntrustedHTMLBase):    
    webClass = "RemoteAccount"
    htmlSummary = True
    title = ""
    twitterId = ''
    mastodonId = ''
    keepAllArticles = False

    def __init__(self):
         self.localArticles = OOBTree()
         self.reset()
         Container.__init__(self)
         
    def reset(self):
         self.crawledToStart = False
         self.minId = None 
         self.maxId = None
        
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
    
    def postAddProcess(self,view = None):
        if self.logoURL:
            getImage(self,self.logoURL)

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

