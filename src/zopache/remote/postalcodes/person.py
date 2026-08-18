from zope.interface import implementer
from zopache.pages.page import Page
from zopache.remote.postalcodes.interfaces import IPerson
from zopache.remote.mastodon.parseid import ParseMastodonId

@implementer(IPerson)
class Person (ParseMastodonId,Page):

    def __init__(self, principal):
        Page.__init__(self)
        self.__name__ = 'p' + principal.__name__        
        self.principal = principal

    @property
    def mastodonId(self):
        return self.principal.handle
