from zope.interface import Interface
from zope import schema
from zopache.pages.interfaces import ILink
from zopache.pages.page import Link
from zopache.ttw.treewidget import TreeField
from zopache.core.viewdecorators import *

class IRSSLink(ILink):

    title = schema.TextLine(
        title = 'Remote Article Name',
        description = 'What is the title of this link?',
        readonly = True,
        required = True,
    )
    remoteURL= schema.URI(
        title = 'URL',
        description = 'The url of the remote article',
        readonly = True,
        required = True,
    )
    
    description= schema.Text(
        title = u'Description',
        description = """A brief introduction of this page.  
                        This is used by the search functions.""",
        required = False,
        default = u'',
        readonly = True,
    )

    source= schema.Text(
        title = 'Content',
        description = 'This is the main content for this page',
        required = False,
        readonly = True,
        default = '',
    )

    category=TreeField(
           title="Category Search",
           description= """You can use this widget to explore the category 
                          tree. It has no impact on the RSS feed. """,
           required = False,
            )    
      
@implementer (IRSSLink)
class RSSLink(Link):
   _category = "" 
   def getCategory(self):
      return self._category
  
   def setCategory(self,value):       
      self._category = value
       
