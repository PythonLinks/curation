
from zope.interface import Interface
from zope import schema
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
from zopache.remote.rssfetch import getArticles
from zopache.remote.irss import IRSS, IJustRSS
from zopache.crud.getimage import getImage
    
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
       new = RSSArticle()
       new.title = unescape (article.title)
       if self.htmlSummary:
             new.source = unescape( article.summary)
       else:
             new.description = article.summary
       
       #if hasattr(article, 'content'):
       #    if len(article.content):
       #      new.source = article.content[0].value
       #else:
       #    new.source = article.summary
       
       new.articleURL = article.link
       if hasattr(article, 'updated_parsed'):
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
          
       #WHEN CREATING A NEW FEED ARTICLES GO AT THEIR PROPER TIME
       #PREVENTS BUNCHING THEM UP.
       new.importTime = new.publishedAt   
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
        if getattr(self,'logoURL', False):
            getImage(self,self.logoURL)
        
    def fetchURLS(self, view = None):    
        urls = [self.rssURL]

        #urls += self.otherFeeds

        result = getArticles(urls)
        for key, value in result.items():
               self.createArticles(value,view)
        view.status='RSS Feeds were downloaded.'
        
    def postProcess(self,view = None):
        Link.postProcess(self, view = view)

    async def processResponse(self, response,view):
          html  =  await response.text()
          feed = feedparser.parse(html)
          entries = feed['entries']
          for article in entries:
                    self.createArticles(entries,view)

@implementer(IJustRSS)
class JustRSS(RSS):
    interface = IJustRSS
    @property
    def title(self):
        return self.parent.title + " RSS Feed"
    
    @property
    def description(self):
        return "This is the RSS feed for " + self.parent.title


    @property
    def remoteURL(self):
        return self.parent.remoteURL
    
    @property
    def twitterId(self):
        return self.parent.twitterId

    

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

