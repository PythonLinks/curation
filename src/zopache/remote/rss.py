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
        
    rssURL = schema.Text(
        title = 'RSS or ATOM URLs',
        description = """List of cateogry feeds.   Many RSS servers 
only list 10 items.  By listing one feed for each category, you can import 
all of your content. Just one URL per line, and pleae include https://""",
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
     title = ""  

       

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
