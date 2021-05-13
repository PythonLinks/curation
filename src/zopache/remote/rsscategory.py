from zope.interface import Interface
from zope import schema


from zopache.pages.page import Page
from zopache.core.viewdecorators import *
from BTrees.LOBTree import LOBTree
from zopache.pages.interfaces import IPageBase

class IRSSCategory(IPageBase):
    title=schema.TextLine(
        title = "RSS Category Name",
        description ="What is the category called?",
        required = True,
        )

    description= schema.Text(
        title = 'Description',
        description = """A brief introduction of this Category.  """,
        required = False,
        default = '',
    )    

@implementer (IRSSCategory)     
class RSSCategory(Page):
    webClass = "RSSCategory"
    title = ""
    description = ""
    source = ""
    def __init__(self):
         self.articlesByTime = LOBTree()
         Page.__init__(self)
        
import crom
from zopache.zmi.interfaces import IURLSegment
@crom.adapter
@crom.sources(IRSSCategory)
@crom.target(IURLSegment)
class IRSSAdaptor(object):
    def __init__(self,context):
        self.context=context   

    def getSegment(self):
        return 'ckedit'

