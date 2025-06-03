from zope.interface import implementer
from zopache.pages.page import Page
from zopache.remote.postalcodes.interfaces import IVoter
from zopache.remote.mastodon.parseid import ParseMastodonId
@implementer(IVoter)
class Voter (ParseMastodonId,Page):

    def __init__(self, principal):
        #self.__parent__ = postalContainer
        Page.__init__(self)
        self.principal = principal

    @property
    def mastodonId(self):
        return self.principal.handle
