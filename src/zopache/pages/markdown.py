from zope.interface import implementer

import mistune

from zopache.pages.page import Page
from zopache.pages.interfaces import IPage
from zopache.pages.interfaces import IMarkdown
from zopache.core.ancestors import Ancestors

@implementer (IMarkdown)
class Markdown (Page,Ancestors):

    def postProcess(self, view = None):        
        self._html = mistune.markdown(self.source)
        Page.postProcess(self, view  = view)

    def postAddProcess(self, view = None):                
        self.postProcess(view = view)
        
    def getHTML(self):
        return self._html

    def html(self):
        return self._html
    





