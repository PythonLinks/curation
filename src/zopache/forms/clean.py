from itertools import islice
from BTrees.OOBTree import OOBTree
from cromlech.security import permissions
from dolmen.container import IBTreeContainer

from zopache.core.viewdecorators import *
from zopache.ttw.interfaces import IBranch
from zopache.core.baseform import Form
from zopache.pages.page import Link
from zopache.remote.rss import IRSS


@form_component
@context(IBTreeContainer)
@target(IView)
@name("clean")
@permissions('Manage')
class Clean(Form):
    title = "Remove OLD Unused RSS Articles"
    subTitle = "Leave 100 most recent articles for each feed."
    def update(self):
        for rssFeed in self.context.rssLeaves():
           rssFeed.removeOldArticles()
           self.status='The Older Articles Were Removed'
           Form.update(self)

