from slugify import slugify

from zopache.crud.addbyurl import  AddByURLForm
from zopache.crud.forms import AddByTitleForm
from zopache.core.interfaces import ITreeSecurity,IUserSecurity
from zopache.core.viewdecorators import *
from zopache.pages.interfaces import IPageBase, IPage
from zopache.remote.rss import  RSS, JustRSS
from zopache.remote.mastodon.interfaces import IAddMastodonAccount, IMastodonAccount
from zopache.remote.mastodon.remoteaccount import MastodonAccount
from zopache.core.page import Page
from zopache.ttw.mail import Notify
from BTrees.OOBTree import OOBTree
from dolmen.container import IBTreeContainer
from zopache.business.exists import Duplicate
from zopache.pages.addanonymous import AddAnonymousPageByTitle

@view_component
@name ('addMastodonAccount')
@target(IView)
@context(IPage)
class AddMsatodonAccount(AddAnonymousPageByTitle,Notify):
     interface = IAddMastodonAccount
     title = "Add an RSS Feed"
     subTitle =""
     count = 0
     factory = MastodonAccount
     layoutName = "UserMenu"
     dataValidators = [Duplicate]
     
     def newURL(self,baseURL):
        return baseURL + '/manage'

     def dataModel(self):

        contextJsonDict =  self.template['rssSchema'].getAsDict()
        result = json.dumps(contextJsonDict)
        return result
   



