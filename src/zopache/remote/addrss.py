from slugify import slugify
import feedparser

from cromlech.security import Unauthorized
from zopache.crud.forms import AddForm
from zopache.core.interfaces import ITreeSecurity,IUserSecurity
from zopache.core.viewdecorators import *
from zopache.pages.interfaces import IPage
from zopache.ttw.interfaces import IContainer
from zopache.remote.rss import IRSS, RSS
from zopache.remote.rsslink import IRSSLink, RSSLink
from zopache.core.breadcrumbs import Breadcrumbs
from zopache.core import View
from zopache.core.page import Page
   
from zopache.crud.forms import AddForm
from zopache.ttw.mail import Notify
from zopache.crud.forms import BaseEditForm
import zopache
from zopache.crud.forms import BaseEditForm
from BTrees.OOBTree import OOBTree

@view_component
@name('addRSS')
@target(IView)
@context(IContainer)
@implementer(IUserSecurity)
class AddRSS(AddForm,Notify):
     interface = IRSS
     title = "Add your RSS Feed"
     subTitle ="Organized By Category"
     count = 0
     factory = RSS
     def getPreamble(self):
         return self.getTemplates()["RssPreamble"].source

     preamble = property (getPreamble)
     
     layoutName = "UserMenu"     
     
     def postAddProcess(self,view = None):
        self.notifyAdminsNewPage()
        self.new.principal = self.request.principal 
        
@view_component
@name('index')
@context(IRSS)
class EvaluateFeed(Page, Breadcrumbs):
   title = "Please Review Your Feed"
   subTitle= 'Are the categories correct?'
   feed = None

   def getRSSLink(self,article):
       return self.getArticles()[article['id']]

   def getCategory(self,article):
       siteRoot = self.getSiteRoot()
       category = self.getRSSLink(article).category
       category = siteRoot[category]
       return category
       
   def update(self):
        self.template = self.getProducts()['Templates']['RSSTemplate']
        self.feed = self.getFeed(self.context)
        
   def getRSSLink(self,entry):
       id = entry['id']
       rssLink = self.getArticles() [id]
       return rssLink

   def getPrincipal(self):
       principal = self.parentWhichImplements(
               zopache.ttw.interfaces.IInternalPrincipal)
       return principal
  
   def getArticles (self):
       siteRoot = self.getSiteRoot()
       if not hasattr(siteRoot,'articles'):
          siteRoot.articles = OOBTree()
       return siteRoot.articles   
                   
   def articleCrumbs(self, article):
       rssLink = self.getRSSLink(article)        
       category = rssLink.category
       root = self.getSiteRoot()
       if category in root:
            item = root [category]
            crumbs = self.breadcrumbsCore(item,showRoot=False)
       else:
            crumbs = "No legal category found."
       return crumbs
  
   def evaluateEntry(self,entry):
       rssLink = self.getRSSLink(entry)
       
       if not 'tags' in entry:
          return "No Category"
     
       if len (entry['tags']) == 0:
           return "No Category"

       siteRoot = self.getSiteRoot()
       if len (entry['tags']) == 1:
          category = entry['tags'][0]['term']  
          category = slugify (category)
          slug = slugify(category)
          if slug in siteRoot:
              rssLink.category = slug
              return "One Good Category"               
          return "Invalid Category"  
       best =(None,1000)          
       if len (entry['tags']) > 1:
          for tag in entry['tags']:
              category = tag['term']  
              slug = slugify (category)
              if slug in siteRoot:
                 category = siteRoot[slug]
                 if category.__class__ == RSS:
                      breakpoint()
                 kids = category.childCategories()
                 length = len (kids)
                 if length < best [1]:
                    best =(slug,length)

          if best [0]==None: 
             return "Multiple Categories, None Good"
          else:          
            rssLink.category = best [0]
            return "Multiple Categories, One Good"


   def getTags(self,entry):
       siteRoot = self.getSiteRoot()
       categories = []
       result = None
       for item in entry["tags"]:
           category = item ['term']
           slug = slugify(category)
           result = None            
           if slug in siteRoot:
              result =  siteRoot[slug]
              self.getRSSLink(entry).category = slug
           categories.append(category)
       return categories
  
   def getFeed(self,rss):
       allFeeds = self.allFeeds = [] 
       allEntries = self.allEntries = {} 
       urls = rss.rssURLs
       urls = urls.split ("\n")
       for url  in urls:
          print (url)  
          feed = feedparser.parse(url)
          allFeeds.append(feed)
          entries = feed['entries']
          for article in entries:
               permalink = article['id']
              allEntries [permalink]=article
       self.entries = allEntries       
       for article in self.entries:
           theId = article['id']
           if not theId in rss.articles:
              rss.createRSSLink(article)
       return self.feed
  
   #No longer used
   def getOneFeed(self,rss):
       articles = self.getArticles()
       self.feed = feedparser.parse(rss.rssURL)
       self.entries = self.feed['entries']
       for article in self.entries:
           theId = article['id']
           if not theId in articles:
              self.createRSSLink(article)
       return self.feed

   def createRSSLink(self,article):
       articles = self.getArticles()
       rss = self.context
       new = RSSLink()
       new.title = article.title
       new.source = article.description
       new.rssURL = article.link
       new.updated = article.updated_parsed
       #new.image = article.image
       theId = article['id']
       articles [theId] = new
       newName = slugify (new.title)
       newName = self.uniqueBothName (newName,rss)
       rss[newName] = new
       new.__parent__ = rss
       new.rss = rss
  
@form_component
@name ('edit')
@context(IRSS)
@implementer(IUserSecurity)
class EditRSS(BaseEditForm):
    pass

from zopache.ttw.html import CkEdit
@form_component
@name ('edit')
@context(IRSSLink)
@implementer(IUserSecurity)
class EditRSSLink(CkEdit):
    pass
