from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.core.getroot import getSiteRoot, getProducts
from dolmen.container import IBTreeContainer
from zopache.remote.rss import IRSS
from cromlech.browser.interfaces import IPublicationRoot
from zopache.core.breadcrumbs import Breadcrumbs
from zopache.remote.rsslink import IRSSLink

@form_component
@context(IPublicationRoot)
@crom.target(IView)
@name("indexRSS")
@permissions('Manage')
class ReIndex(Form,Breadcrumbs):
    title = "Index the RSS Link Objects"
    def update(self):
           siteRoot = self.getSiteRoot()
           articles = self.resetArticles()
           self.status='RSSLinks were indexed'
           Form.update(self)
           self.indexArticles(articles,branch = siteRoot)

    def indexArticles(self,articles,branch = None):
        for item in branch.values():
            if IRSSLink.providedBy(item):
                articles[item.permaLink]=item
            if IBTreeContainer.providedBy(item):    
                self.indexArticles(articles, branch = item)
