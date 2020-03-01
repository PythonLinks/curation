from zope.interface import implementer

import mistune

from zopache.pages.page import Page
from zopache.pages.interfaces import IPage
from zopache.pages.interfaces import IMarkdown

@implementer (IMarkdown)
class Markdown (Page):

    def postProcess(self, view = None):        
        self._html = mistune.markdown(self.source)

    def postAddProcess(self, view = None):                
        self.postProcess(view = view)
        
    def html(self):
        return self._html
      





