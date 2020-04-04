from zope import schema
from zope.interface import Interface

from zopache.pages.page import Page
from zopache.core.viewdecorators import *
from zopache.remote.ivideo import IBasicVideo, IPrincipalVideo
from zopache.pages.interfaces import ILink
from zopache.pages.page import Link
from BTrees.OOBTree import OOBTree
from zopache.core import Leaf,Container
from zopache.ttw.treewidget import TreeField
from zopache.crud.interfaces import ILeaf
from zopache.core.uniquename import UniqueName
from zopache.remote.rsslink import IRSSLink

class IRSS(ILeaf):
    title=schema.TextLine(
        title = "RSS Feed Name",
        description ="Please give it a name",
        required = True,
        )
        
    rssURL = schema.URI(
        title = 'RSS or ATOM URL',
        description = 'Wheree is this feed? Please include https://',
        required = True,
    )      

    category=TreeField(
           title="Category Search",
           description= """You can use this widget to explore the category 
                          tree. It has no impact on the RSS feed. """,
           required = False,
            )    
    
import feedparser    
        
@implementer (IRSS)     
class RSS(Leaf):
   
   def __init__(self):
       Leaf.__init__
       articles = OOBTree()

   def getFeed(self):
       feed = feedparser.parse(self.rssURL)
       for article in self.entries():
           id = article['id']
           if not id in articles:
              self.createRSSLink(article) 
       return feed

   def createRSSLink(self,article):
       new = RSSLink()
       new.title = article.title
       new.source = article.description
       new.link = article.link
       new.updated = article.updated_parsed
       self.articles [id] = new
       newName = self.uniqueBothName (new.title,self)
       self [newName] = new
       new.__parent__ = self
       new.rss = self       
   
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
       

import crom
from zopache.zmi.interfaces import IURLSegment
@crom.adapter
@crom.sources(IRSS)
@crom.target(IURLSegment)
class ICSSFolderAdaptor(object):
    def __init__(self,context):
        self.context=context   

    def getSegment(self):
        return 'edit'
