#CURRENTLY JUST TO A SINGLE PERSON
#CURRENTLY ONLY USES MAIL QUEUE
from time import time

from zopache.core.viewdecorators import *
from zopache.core import Leaf, Container
from zopache.crud.interfaces import ILeaf, IContainer
from zopache.pages.interfaces import IPageBase
from zopache.core.interfaces import ITreeSecurity
from zopache.core.transactionnote import TransactionNote

from zopache.remote.mastodon.interfaces import IServer    
@implementer(IServer)
class Server(Container):
    webClass = "OauthServer"
    def mastodonDomainName(self):
        return self.__name__.lower()
