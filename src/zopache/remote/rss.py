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


class IRSS(ILink):
    title=schema.TextLine(
        title = "RSS Feed Name",
        description ="What is the web site called?",
        required = True,
        )

    twitterId=schema.TextLine(
        title = "Twitter Id",
        description ="""Without the "@" sign?""",
        required = False,
        )    
    
    rssURL=schema.URI(
        title = "Primary RSS URI",
        description ="""This is the source of new articles.  
              Please include "https://" or "http://".""",
        required = True,
        )

    rssURL=schema.Bool(
        title = "htmlSummary",
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

     def fetchArticles (self,view = None):               
       feed = feedparser.parse(self.rssURL)
       entries = feed['entries']
       self.createArticles(entries,view)
       
     def createArticles(self,entries,view):
       globalArticles= self.getSiteRoot().globalArticles
       for article in entries:
           theId = article['id']
           if not theId in globalArticles:
              self.createOneArticle(article,view )

     def postAddProcess(self,view = None):
        self.fetchArticles(view)
        Link.postAddProcess(self,view = view)
        
     def postProcess(self,view = None):
        #self.fetchArticles(view)
        Link.postProcess(self, view = view)
        
              
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

