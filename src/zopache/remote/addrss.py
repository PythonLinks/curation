from slugify import slugify
import feedparser
import time

from cromlech.security import Unauthorized
from zopache.crud.forms import AddByTitleForm, AddByURLForm
from zopache.core.interfaces import ITreeSecurity,IUserSecurity
from zopache.core.viewdecorators import *
from zopache.pages.interfaces import IPage
from zopache.ttw.interfaces import IContainer
from zopache.remote.rss import IRSS,  IRSSPage, RSS
from zopache.remote.rssarticle import IRSSArticle, RSSArticle
from zopache.core.breadcrumbs import Breadcrumbs
from zopache.core import View
from zopache.core.page import Page
   
from zopache.crud.forms import AddNamedForm
from zopache.ttw.mail import Notify
from zopache.crud.forms import BaseEditForm
import zopache
from zopache.crud.forms import BaseEditForm
from BTrees.OOBTree import OOBTree
from zopache.remote.downloadrss import doit

import feedparser
def processRssResponse(url,html):
          print (html[: 10])
          allEntries = {}          
          feed = feedparser.parse(html)
          entries = feed['entries']
          print ("LEN",len(entries))
          print (type(entries))
          for article in entries:
               permalink = article['id']
               print ("Perma",permalink)
          return  ('Success', url, html)

def processImageResponse(url,response):
          print (url)
          return  ('Success' ,url,response)

class Base(object):
   # FOR A NEW RSS FEED       
   def createRSSLink(self,article):
       rssFeed = self.new      
       self.createRSSLinkCore(rssFeed,article)
        
   def createRSSLinkCore(self,rssFeed,article):
             
       new = RSSArticle()
       new.title = article.title
       new.descriptin = article.summary
       if len(article.content):
           new.source = article.content[0].value   
       new.articleURL = article.link
       new.updated = article.updated_parsed
       if 'image' in article:      
           new.image = article.image
           
       theId = article['id']
       new.permaLink = theId
       if hasattr(article,"published_parsed"):
          new.publishedAt = time.mktime( article["published_parsed"])
       else:
          new.publishedAt = time.time()
       newName = slugify (new.title)
       newName = self.uniqueBothName (rssfeed,newName)
       rssFeed[newName] = new

       #Global List
       globalArticles = self.getRemoteLinks()
       globalArticles [theId] = new

       #LocalList
       rssFeed.articles[theId] = new
       new.__parent__ = rssFeed
       new.rssFeed = rssFeed          
       new.partialPostProcess(view = self)

   def getOneFeedCore (self,context):               
       globalArticles = self.getRemoteLinks()
       self.feed = feed = feedparser.parse(context.rssURL)
       context.description = feed.feed.subtitle
       self.entries = self.feed['entries']
       for article in self.entries:
           theId = article['id']
           if not theId in globalArticles:
              self.createRSSLink(article)

@view_component
@name('addNewsSite')
@target(IView)
@context(IContainer)
@implementer(ITreeSecurity)
class AddRSSByURL(AddByURLForm,Notify,Base):
     factory = RSS
              
@view_component
@name('addRSS')
@target(IView)
@context(IContainer)
@implementer(ITreeSecurity)
class AddRSS(AddByTitleForm,Notify,Base):
     interface = IRSS
     title = "Add an RSS Feed"
     subTitle ="Organized By Category"
     count = 0
     factory = RSS
     
     #def getPreamble(self):
     #    return self.getTemplates()["RssPreamble"].source
     #preamble = property (getPreamble)
     
     layoutName = "UserMenu"
     
     def newURL(self,baseURL):
        return baseURL + '/manage'
   
     def postAddProcess(self,view = None):
        #self.getOneFeedCore(self.new)
        self.notifyAdminsNewPage()
        self.context.recalculateRootJSON()
        
         
     def getOneFeed(self):
         self.getOneFeedCore(self.context)         


from zopache.core.baseform import Form
from zope.interface import Interface
@view_component
@name('updateRSS')
@target(IView)
@context(IRSS)
@implementer(ITreeSecurity)
class UPDATERSS(Form,Base):
     interface = Interface
     title = "Update an RSS Feed"
     subTitle ="Download new Articles Category"
     count = 0
     layoutName = "UserMenu"
     def update(self):
        self.status='RSS Was updated'
           
     def postProcess(self,view = None):
        self.getOneFeedCore(self.new)
        self.context.recalculateRootJSON()
        


         
@form_component
@name ('edit')
@context(IRSS)
@implementer(IUserSecurity)
class EditRSS(BaseEditForm):
    pass

from zopache.ttw.htmlviews import CkEdit
@form_component
@name ('edit')
@context(IRSSArticle)
@implementer(IUserSecurity)
class EditRSSLink(CkEdit):
    pass
