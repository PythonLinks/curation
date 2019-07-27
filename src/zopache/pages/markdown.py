from zopache.pages.page import Page
from zopache.pages.interfaces import IMarkdown
from zope.interface import implementer

import mistune

@implementer (IMarkdown)
class Markdown (Page):

    def postEditProcess(self):        
        self._html = mistune.markdown(self.source)

    def html(self):
        return self._html
      




