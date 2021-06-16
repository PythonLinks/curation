from BTrees.OOBTree import OOBTree
from cromlech.security import permissions
from itertools import islice
from zopache.core.viewdecorators import *
from zopache.ttw.interfaces import IBranch
from zopache.core.baseform import Form
from zopache.pages.interfaces import IRootPage
from zopache.pages.page import Link
from zopache.remote.rss import IRSS

@form_component
@context(IRSS)
@target(IView)
@name("clean")
@permissions('Manage')
class Clean(Form):
    title = "Remove RSS Articles"
    subTitle = ""
    def update(self):
           context = self.context
           articles = []
           for value in context.values():
               if self.className(value) == "RSSArticle":               
                   articles.append(value)
               
           for article in articles:    
               article.preDeleteProcess(self)
               del article.parent [article.name]
           
           orphans = []    
           for key,value in context.localArticles.items():
               if value.parent == None:
                   orphans.append[key]
           #for key in orphans:
           #    print (key)
           #    del context.localArticles [key]
           self.status='The Articles Were Removed'
           Form.update(self)

