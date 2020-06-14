from zope import schema
from zope.interface import Interface
from slugify import slugify

from zopache.pages.page import Link, Page
from zopache.core.viewdecorators import *
from zopache.remote.ivideo import IBasicVideo, IPrincipalVideo
from zopache.pages.page import Page
from zopache.crud.interfaces import IContainer
from zopache.core.uniquename import UniqueName
from BTrees.OOBTree import OOBTree
from zopache.pages.interfaces import IPage

class IRSS(Interface):
    title=schema.TextLine(
        title = "RSS Feed Name",
        description ="What is the web site called?",
        required = True,
        )
    
    rssURL=schema.URI(
        title = "Primary RSS URI",
        description ="""This is the source of new articles.  
              Please include "https://" or "http://".""",
        required = True,
        )    

#    otherFeeds = schema.Text(
#        title = 'Other RSS URLs',
#        description =""" Many RSS Feeds only allow 10 items, which makes it 
#impossible to access all of your articles. Here is a way around that limitation. 
#Many WebSites have categories, each 
#with their own RSS feeds, each with less than 10 items.  So you can include
#those other category rss feeds here, and import all of your content.   
#Just one URL per line, and please include https://""",
#        required = False,
#    )      



                          

class IRSSPage (IPage,IRSS):
      pass
    


from zopache.core.getroot import getSiteRoot    
@implementer (IRSS)     
class RSS(Link):
     webClass = "RSS"
     title = ""
     def __init__(self):
         self.articles = OOBTree()
         Link.__init__(self)

import crom
from zopache.zmi.interfaces import IURLSegment
@crom.adapter
@crom.sources(IRSS)
@crom.target(IURLSegment)
class IRSSAdaptor(object):
    def __init__(self,context):
        self.context=context   

    def getSegment(self):
        return 'manage'

