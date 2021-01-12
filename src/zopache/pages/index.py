from zopache.core.viewdecorators import *
from cromlech.webob.response import Response
from dolmen.view import  make_view_response
from zopache.pages.interfaces import ILayoutView
from zopache.core.breadcrumbs import Breadcrumbs
from zopache.ttw.htmlviews import Index

@view_component
@name('index')

@context(ILayoutView)
class PageIndex(Index):
    def update(self):
        self.zopacheTemplate = self.getIndex()

    def getIndex(self):
           return self.layoutAcquire('index')
        
    def render(self):

        content = Index.render(self)
        zopacheTemplate = self.getIndex()
        if not hasattr(zopacheTemplate,'layout'):
            return content
        layout = zopacheTemplate.layout
        if layout == "":
            return content
        template = self.parentalAcquire(layout, context = zopacheTemplate)
        view = self
        return template.__call__(view,content=content)
    
        self.template = self.parentalAcquire(layout, context = zopacheTemplate)
        view = self
        return template.__call__(view,content=content)
    
