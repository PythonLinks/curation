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

preamble ="""     
<p>This is an RSS <bold>dis</bold>agregator. It takes your flat list 
of articles and
sorts them into categories.  Each category brimgs together 
articles from multiple blogs.  This way the user can easily find articles
on the same or related topics.
</p> 
<p> 
To make this work, you mark
your articles with the correct label or category, and the software then imports
your rss feed.  At the bottom of this page, you will see a tree widget with 
available categories.  Please <a href = "/contact">contact me </a>, if you 
would like to propose any change in the taxonomy.  I am generally happy 
to accomodate your needs. 
</p>
<p>  To make this work we need to cooperate.  A basic principal in human 
factors is that there should be no more than about 7 items in any category. 
So when a category gets too large, it needs to be split up.  The way to 
get your articles into the root of the tree is to write a good article, 
so that everyone upvotes your articles. 
The way to do
is to place your article in the appropriate leaf of the tree, and then get 
lots of upvotes.  Your articles will float up based on the search algorithms.  
You are rated on the upvotes and downvotes of all of your articles. 
</p>

<p>
After you submit your rss feed you will see a page reviewing the quality of 
feed.  When you are satisfied with the feed, please <a href = "/contact">contact me </a> so that I can approve your feed and import the articles. 
</p>
"""
from zopache.crud.forms import AddForm

@view_component
@name('addRSS')
@target(IView)
@context(IContainer)
@implementer(IUserSecurity)
class AddRSS(AddNamedForm):
     interface = IRSS
     title = "Add an RSS Feed"
     subTitle ="More instructions after you submit."
     count = 0
     factory = RSS
     preamble = preamble                    
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
