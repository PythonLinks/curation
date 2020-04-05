from slugify import slugify
import feedparser

from cromlech.security import Unauthorized
from zopache.crud.forms import AddNamedForm
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


     

@view_component
@name('addRSS')
@target(IView)
@context(IContainer)
@implementer(IUserSecurity)
class AddRSS(AddNamedForm,Notify):
     interface = IRSS
     title = "Add your RSS Feed"
     subTitle ="Organized By Category"
     count = 0
     factory = RSS
     def getPreamble(self):
         return self.getTemplates()["RssPreamble"].source

     preamble = property (getPreamble)
     
     layoutName = "UserMenu"     
     
     def newName(self,data):
        name = 'MyRSSFeed'
        context = self.context
        newName=self.uniqueContainerName(context,name,ofType="#")
        return newName
   
     def postAddProcess(self,view = None):
        self.notifyAdminsNewPage()

        
@view_component
@name('index')
@context(IRSS)
class EvaluateFeed(Page, Breadcrumbs):
   title = "Please Review Your Feed"
   subTitle= 'Are the categories correct?'
   feed = None

   def getRSSLink(self,article):
       return self.context.articles [article['id']]

   def getCategory(self,article):
       siteRoot = self.getSiteRoot()
       category = self.getRSSLink(article).category
       category = siteRoot[category]
       return category.title
       
   def update(self):
        self.template = self.getProducts()['Templates']['RSSTemplate']
        self.feed = self.getFeed(self.context)
        
   def getRSSLink(self,entry):
       id = entry['id']
       rssLink = self.context.articles [id]
       return rssLink
                     
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
          
       if len (entry['tags']) > 1:
          for tag in entry['tags']:
              category = tag['term']  
              slug = slugify (category)
              if slug in siteRoot:
                  rssLink.category = slug                   
                  return "Multiple Categories, One Good"
          return "Multiple Categories, None Good"
       return "Something went wrong" 

   def getCategories(self,entry):
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
       self.feed = feedparser.parse(rss.rssURL)
       self.entries = self.feed['entries']
       for article in self.entries:
           theId = article['id']
           if not theId in rss.articles:
              rss.createRSSLink(article)
       return self.feed
 

@form_component
@name ('edit')
@context(IRSS)
class EditRSSForm(BaseEditForm):
    pass

from zopache.ttw.html import CkEdit
@form_component
@name ('edit')
@context(IRSSLink)
class EditRSSLinkForm(CkEdit):
    pass
