from zope import schema
from zope.interface import Interface
from slugify import slugify

from zopache.pages.page import Page
from zopache.core.viewdecorators import *
from zopache.remote.ivideo import IBasicVideo, IPrincipalVideo
from zopache.pages.interfaces import ILink
from zopache.pages.page import Link
from BTrees.OOBTree import OOBTree
from zopache.core import Container
from zopache.ttw.treewidget import TreeField
from zopache.crud.interfaces import IContainer
from zopache.core.uniquename import UniqueName
from zopache.remote.rsslink import IRSSLink, RSSLink

class IRSS(IContainer):
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
    


from zopache.core.getroot import getSiteRoot    
@implementer (IRSS)     
class RSS(Container,UniqueName):
   
   def __init__(self):
       Container.__init__(self)
       self.articles = OOBTree()


   def createRSSLink(self,article):
       new = RSSLink()
       new.title = article.title
       new.source = article.description
       new.rssURL = article.link
       new.updated = article.updated_parsed
       theId = article['id']
       self.articles [theId] = new
       newName = slugify (new.title)
       newName = self.uniqueBothName (new.title,self)
       self [newName] = new
       new.__parent__ = self
       new.rss = self
       

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
