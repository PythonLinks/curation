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
    title = "Remove OLD Unused RSS Articles"
    subTitle = "Leave 100 most recent articles for each feed."
    def update(self):
           rss = self.context
           rss.removeOldArticles()
           self.status='The Older Articles Were Removed'
           Form.update(self)

