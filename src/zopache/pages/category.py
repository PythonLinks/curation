from zopache.pages.page import Page
from zopache.core.viewdecorators import *
from BTrees.LOBTree import LOBTree
from zopache.pages.interfaces import ICategory

@implementer (ICategory)     
class Category(Page):
    webClass = "Category"
    title = ""
    description = ""
    source = ""
    def getImportTime(self):
        return int(self.creationTime)
    importTime = property(getImportTime)
    
"""        
import crom
from zopache.zmi.interfaces import IURLSegment
@crom.adapter
@crom.sources(ICategory)
@crom.target(IURLSegment)
class IRSSAdaptor(object):
    def __init__(self,context):
        self.context=context   

    def getSegment(self):
        return 'ckedit'
"""
