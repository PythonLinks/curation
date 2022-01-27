import time
from cromlech.security import permissions
from dolmen.container import IBTreeContainer
from zopache.core.viewdecorators import *
from zopache.core.baseform import Form


@form_component
@context(IBTreeContainer)
@target(IView)
@name("curated")
@permissions('Manage')
class Clean(Form):
    title = "Record that the articles were curated."
    subTitle = ""
    def update(self):
        self.getSiteRoot().lastCuratedAt = time.time()
        self.status='Curation End Time was recorded.'

        
