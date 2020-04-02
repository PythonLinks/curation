from slugify import slugify

from cromlech.security import Unauthorized
from zopache.crud.forms import AddNamedForm
from zopache.core.interfaces import ITreeSecurity,IUserSecurity
from zopache.core.viewdecorators import *
from zopache.pages.interfaces import IPage
from zopache.ttw.interfaces import IContainer
from zopache.remote.rss import IRSS, RSS
from zopache.core.breadcrumbs import Breadcrumbs
from zopache.core import View
from zopache.core.page import Page

from zopache.crud.forms import AddForm

@view_component
@name('addRSS')
@target(IView)
@context(IContainer)
@implementer(IUserSecurity)
class AddRSS(AddNamedForm):
     interface = IRSS
     title = "Add an RSS Feed"
     subTitle ="Organized By Category"
     count = 0
     factory = RSS
     def getPreamble(self):
         return self.getTemplates()["RssPreamble"].source

     preamble = property (getPreamble)
     
     layoutName = "UserMenu"     
     
     def newName(self,data):
        return 'MyRSSFeed'
   
@view_component
@name('index')
@context(IRSS)
class EvaluateFeed(Page, Breadcrumbs):
   title = "Review Your Feed"
   subTitle='Please categorize your content correctly.'   
   feed = None
   def update(self):
        self.template = self.getProducts()['Templates']['RSSTemplate']
        self.feed = self.context.getFeed()
        self.entries = self.feed ['entries']
                     
   def getFirstGoodCategory(self,entry):
       siteRoot = self.getSiteRoot()
       categories = []
       result = None
       for item in entry["tags"]:
           category = item ['term']
           slug = slugify(category)
           if slug in siteRoot:
              result = category
              self.node = siteRoot[slug]
           else:   
              categories.append(category)
       return (result, categories)

   def articleCrumbs(self, article):
       category = self.getFirstGoodCategory(article)[0]
       slug = slugify (category)
       root = self.getSiteRoot()
       item = root [slug]
       crumbs = self.breadcrumbsCore(item,showRoot=False)
       return crumbs
  
   def evaluateEntry(self,entry):
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
              return "One Good Category"               
          return "Invalid Category"  
          
       if len (entry['tags']) > 1:
          for tag in entry['tags']:
              category = tag['term']  
              slug = slugify (category)
              if slug in siteRoot:
                  return "Multiple Categories, One Good"
          return "Multiple Categories, None Good"
       return "Something went wrong" 

from zopache.crud.forms import BaseEditForm

@form_component
@name ('edit')
@context(IRSS)
@title("Edit")
class EditForm(BaseEditForm):
    pass
