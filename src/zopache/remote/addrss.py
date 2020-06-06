from slugify import slugify
import feedparser
import time

from cromlech.security import Unauthorized
from zopache.crud.forms import AddByTitleForm
from zopache.core.interfaces import ITreeSecurity,IUserSecurity
from zopache.core.viewdecorators import *
from zopache.pages.interfaces import IPage
from zopache.ttw.interfaces import IContainer
from zopache.remote.rss import IRSS, IAddRSS, RSS
from zopache.remote.rsslink import IRSSLink, RSSLink
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
def processRssResponse(html):          
          feed = feedparser.parse(html)
          entries = feed['entries']
          print ("LEN",len(entries))
          print (type(entries))
          for article in entries:
               permalink = article['id']
               print ("Perma",permalink)
               allEntries [permalink]=article          
          return  ('Success' ,url)

          



@view_component
@name('addRSS')
@target(IView)
@context(IContainer)
@implementer(IUserSecurity)
class AddRSS(AddByTitleForm,Notify):
     interface = IAddRSS
     title = "Add your RSS Feed"
     subTitle ="Organized By Category"
     count = 0
     factory = RSS
     def getPreamble(self):
         return self.getTemplates()["RssPreamble"].source

     preamble = property (getPreamble)
     
     layoutName = "UserMenu"
     
     def newURL(self,baseURL):
        return baseURL + '/evaluate'
   
     def postAddProcess(self,view = None):
        self.notifyAdminsNewPage()
        self.new.principal = self.__parent__ 

from dolmen.view import View
from cromlech.webob.response import Response
from dolmen.view import  make_view_response

@view_component
@name('evaluate')
@context(IRSS)
class EvaluateFeed(View, Breadcrumbs):
   title = "Please Review Your Feed"
   subTitle= 'Are the categories correct?'
   feed = None
   responseFactory = Response
   make_response = make_view_response
    
   def render(self):
       return self.template.render(self,context=context,view = self)
       
   def getRSSLink(self,article):
            self.getArticles()[article['id']]

       
   def getCategory(self,article):
       siteRoot = self.getSiteRoot()
       category = self.getRSSLink(article).category
       category = siteRoot[category]
       return category

   def getPossibleCategory(self,article):
       siteRoot = self.getSiteRoot()
       category = self.getRSSLink(article).possibleCategory
       category = siteRoot[category]
       return category  
       
   def update(self):
        self.template = self.getProducts()['Templates']['RSSTemplate']
        self.feed = self.getFeed(self.context)
        self.getGoodAndBadArticles()
        return self
   
   def getRSSLink(self,entry):
       id = entry['id']
       rssLink = self.getArticles() [id]
       return rssLink

   def getPrincipal(self):
       principal = self.parentWhichImplements(
               zopache.ttw.interfaces.IInternalPrincipal)
       return principal
  
   def isGoodRSSLink(self,rssLink):
       cat = self.getCategoryObject(rssLink)
       if cat == None:
           return False  
       if len(cat.childCategories())  ==0:
           return True
       return False
  
   def getCategoryObject(self,rssLink):
        if hasattr(rssLink,'category'):
            category = rssLink.category
        elif hasattr(rssLink,'possibleCategory'):
            category = rssLink.possiblecategory
        else:
             return None
        if category != '':
             siteRoot = self.getSiteRoot()
             if category in siteRoot:
                 categoryObject = siteRoot[category]
                 return categoryObject
        return None     
           
   def getGoodAndBadArticles(self):
       bad  = []
       good = []
       for item in self.entries:
          rssLink = self.getRSSLink(item)
          if self.isGoodRSSLink(rssLink):
              print (item.title)  
              print ("good", item.category)
              print ("")
              good.append(item)        
          else:
              print ("bad",item.title)  
              bad.append(item)
       self.good = good
       self.bad = bad



        
   def articleCrumbs(self, article):
       rssLink = self.getRSSLink(article)
       item = self.getCategoryObject(article)
       if item != None:
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
          slug = slugify(category)
          print (slug)
          if slug in siteRoot:
              category = siteRoot [slug]
              parent = category.__parent__
              siblings = parent.childCategories()
              if len (siblings) > 0:
                  rssLink.possibleCategory = slug
                  return "Could Be Better"   
              rssLink.category = slug
              return "One Good Category"               
          return "Invalid Category"

       best =(None, #Category Name
              1000  #Number of Children
               )          
       if len (entry['tags']) > 1:
          for tag in entry['tags']:
              category = tag['term']  
              slug = slugify (category)
              if slug in siteRoot:
                 category = siteRoot[slug]
                 kids = category.childCategories()
                 length = len (kids)
                 if length < best [1]:
                    best =(slug,length)                    
          if best [0]==None: 
             return "Multiple Categories, None Good"
          elif best[1] > 0:      
            rssLink.possibleCategory = best[1]
            return "Multiple Categories, None Good"
          elif best[1] == 0:      
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
       allURLS = []
       allURLS.append (rss.rssFeed)
       urls = rss.otherFeeds
       urls = urls.splitlines ()
       for url  in urls:
          url.strip()  
          print ("FEED =",url)
          allURLS.append (url)
       self.entries = doit(allURLS,processRssResponse)

       self.entries =  [ v for v in self.entries. values() ]

       for article in self.entries:
           theId = article['id']
           if not theId in self.getArticles():
              self.createRSSLink(article)
       return self.feed
  
   #No longer used
   """
   def getOneFeed(self,rss):
       articles = self.getArticles()
       self.feed = feedparser.parse(rss.rssURL)
       self.entries = self.feed['entries']
       for article in self.entries:
           theId = article['id']
           if not theId in articles:
              self.createRSSLink(article)
       return self.feed
   """
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
       new.permaLink = theId
       if hasattr(article,"published_parsed"):
          new.publishedAt = time.mktime( article["published_parsed"])
       else:
          new.publishedAt = time.time()
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

from zopache.ttw.htmlviews import CkEdit
@form_component
@name ('edit')
@context(IRSSLink)
@implementer(IUserSecurity)
class EditRSSLink(CkEdit):
    pass
