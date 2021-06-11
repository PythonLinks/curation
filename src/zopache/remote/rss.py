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
from bs4 import BeautifulSoup
from zopache.remote.irss import IRSS, IJustRSS
from zopache.remote.rssdownload import fetchAll
from zopache.core.getroot import getSiteRoot
from zopache.crud.getimage import getImage

@implementer (IRSS)     
class RSS(Link,UniqueName):
    webClass = "RSS"
    htmlSummary = False
    title = ""
    rssApproved = True
    def __init__(self):
         self.localArticles = OOBTree()
         Link.__init__(self)

    def parseHTML(self,html):
        if not self.htmlSummary:
            return html
        
        soup = BeautifulSoup(html, 'html.parser')
        try:
            
           text = soup.text
           length = len(text)
           if length <= 300:
              return text
           else:
              for i in range(300,length):
                  if text[i]==' ':
                     break
              result = text [0:i-1] +  '...'
              print (result)
              return result
           
        except:
           return ""
       
    # FOR A NEW RSS FEED       
    def createOneArticle(self,article,view):
       new = RSSArticle()
       new.title = unescape (article.title)
       if self.htmlSummary:
           unescaped = unescape( article.summary)
           result  = self.parseHTML(unescaped)
           new.description = result
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
        self.fetchAll(view = view)
        if self.logoURL:
            getImage(self,self.logoURL)
        
    def fetchAll(self, view = None):    
        urls = [self.rssURL]

        #urls += self.otherFeeds
        result = fetchAll(urls,view)
        view.status='RSS Feeds were downloaded.'
        
    def postProcess(self,view = None):
        Link.postProcess(self, view = view)

    async def processResponse(self, session, response,view):
          html  =  await response.text()
          feed = feedparser.parse(html)
          entries = feed['entries']
          self.createArticles(entries,view)
          print (self.name + "RSS WAS CREATED")
          
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

