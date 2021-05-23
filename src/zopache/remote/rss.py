
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

class IRSSBase(Interface):
    pass

class IJustRSS(IRSSBase):
    rssURL=schema.URI(
        title = "Primary RSS URI",
        description ="""This is the source of new articles.  
              Please include "https://" or "http://".""",
        required = True,
        )

    htmlSummary=schema.Bool(
        title = "Is the Summary HTML?",
        description ="For those sources where the summary contains html tags",
        required = False,
        default = False,
        )


class IRSS(IRSSBase):
    title=schema.TextLine(
        title = "RSS Feed Name",
        description ="What is the web site called?",
        required = True,
        )

    description= schema.Text(
        title = 'Description',
        description = """A brief introduction of this RSS Source.  """,
        required = False,
        default = '',
    )    

    twitterId=schema.TextLine(
        title = "Twitter Id",
        description ="""Without the "@" sign?""",
        required = False,
        )
    
    remoteURL= schema.URI(
        title = 'URL',
        description = """A URL That this page refers to. 
             Please include 'https://'""",
        required = False,
    )
    
    rssURL=schema.URI(
        title = "Primary RSS URI",
        description ="""This is the source of new articles.  
              Please include "https://" or "http://".""",
        required = True,
        )

    htmlSummary=schema.Bool(
        title = "Is the Summary HTML?",
        description ="For those sources where the summary contains html tags",
        required = False,
        default = False,
        )        

    
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
        return 'ckedit'

