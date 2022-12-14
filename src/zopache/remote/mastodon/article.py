
from zope.interface import implementer
from zopache.remote.rssarticle import BaseArticle
from zopache.remote.mastodon.interfaces import ITootedArticle

@implementer (ITootedArticle)
class TootedArticle(BaseArticle):
    def getAuthor(self,view ):
        breakpoint()

    def preDeleteProcess(self,view):
        pass

    def postAddProcess (self, view = None):
       self.description += " " + view.context.mastodonId
