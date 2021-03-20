from zope import schema
from zope.interface import Interface
from slugify import slugify
import feedparser
from html import unescape

import time
from zopache.pages.page import Link
from zopache.core.viewdecorators import *
from zopache.remote.ivideo import IBasicVideo, IPrincipalVideo
from zopache.crud.interfaces import IContainer
from zopache.core.uniquename import UniqueName
from BTrees.OOBTree import OOBTree
from zopache.pages.interfaces import ILink
from zopache.remote.rssarticle import RSSArticle
from zopache.crud.getimage import getImage
from zopache.remote.rssdownload import getRSS

class IRSS(ILink):
    pass

    
class IRSSPage (IRSS):
      pass
    
from zopache.core.getroot import getSiteRoot    
@implementer (IRSS)     
class RSS(Link,UniqueName):
    webClass = "RSS"
    htmlSummary = False
    title = ""
    def __init__(self):
         self.localArticles = OOBTree()
         Link.__init__(self)
          
    # FOR A NEW RSS FEED       
    def createOneArticle(self,article,view):
       breakpoint()
       new = RSSArticle()
       new.title = unescape (article.title)
       new.description = unescape( article.summary)
       #if hasattr(article, 'content'):
       #    if len(article.content):
       #      new.source = article.content[0].value
       #else:
       #    new.source = article.summary
       
       new.articleURL = article.link
       new.updated = article.updated_parsed

       if 'image' in article:      
           new.image = article.image

       if 'links' in article:
           new.links = article.links
           
       theId = article['id']
       new.permaLink = theId
       if hasattr(article,"published_parsed"):
          new.publishedAt = time.mktime( article["published_parsed"])
       else:
          new.publishedAt = time.time()
       newName = slugify (new.title)
       newName = self.uniqueBothName (self,newName)
       self[newName] = new

       #LocalList
       self.localArticles[theId] = new
       new.__parent__ = self
       new.rssFeed = self          
       new.postAddProcess(view )

    def createArticles(self,entries,view):
       globalArticles= self.getSiteRoot().globalArticles
       for article in entries:
           theId = article['id']
           if not theId in globalArticles:
              self.createOneArticle(article,view )

    def postAddProcess(self,view = None):
        Link.postAddProcess(self,view = view)
        self.fetchURLS(view = view)
        if self.logoURL:
            getImage(self,self.logoURL)
        
    def fetchURLS(self, view = None):    
        urls = [self.rssURL]

        urls += self.otherFeeds
        result = getRSS(urls)
        for key, value in result.items():
               self.createArticles(value,view)
        view.status='RSS Feeds were downloaded.'
        
    def postProcess(self,view = None):
        Link.postProcess(self, view = view)
        
    def getRemoteURL(self):
        return self.rss["remoteURL"]

    def setRemoteURL(self):
        self.rss["remoteURL"] = value
    
    def getRssURL(self):
        return self.rss["rssURL"]
    
    def setRssURL(self):
        self.rss["rssURL"] = value
   
    def getLogoURL(self):
        return self.rss["logoURL"]
    
    def setLogoURL(self):
        self.rss["logoURL"] = value                

    def getTitle(self):
        return self.rss["title"]

    def setTitle(self,value):
        self.rss["title"] = value


    def getTwitterId(self):
        return self.rss["twitterId"]

    def setTwitterId(self,value):
        self.rss["twitterId"] = value        
        
    def getDescription(self):
        return self.rss["description"]

    def setDescription(self,value):
        self.rss["description"] = value

    def getSource(self):
        self.rss["english"]["source"]

    def setSource(self,value):
        self.rss["source"] = value                

    remoteURL = property(getRemoteURL,setRemoteURL)
    rssURL = property(getRssURL,setRssURL)
    logoURL = property(getLogoURL, setLogoURL)    
    twitterId = property(getTwitterId,setTwitterId)        
    title = property(getTitle,setTitle)
    description = property(getDescription,setDescription)
    source = property(getSource,setSource)        
              
import crom
from zopache.zmi.interfaces import IURLSegment
@crom.adapter
@crom.sources(IRSS)
@crom.target(IURLSegment)
class IRSSAdaptor(object):
    def __init__(self,context):
        self.context=context   

    def getSegment(self):
        return 'manage'

