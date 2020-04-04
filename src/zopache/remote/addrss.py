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
from zopache.ttw.mail import Notify

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
   
   def update(self):
        self.template = self.getProducts()['Templates']['RSSTemplate']
        self.feed = self.context.getFeed()

   def getEntries (self,feed):
       entries = feed['entries']
       return entries

  get RSSLink(self,entry):
       id = entry['id']
       rssLink = self.context.articles [id]
       return rssLink
                     


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
