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

class IRSS(ILeaf):
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
       return feed
   
   def entries (self,feed):
       entries = feed['entries']
       return entries
       

       

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
