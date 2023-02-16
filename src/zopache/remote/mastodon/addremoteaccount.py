from slugify import slugify

from zopache.crud.forms import AddByTitleForm, TreeSecurityAddForm
from zopache.core.interfaces import ITreeSecurity
from zopache.core.viewdecorators import *
from zopache.pages.interfaces import IPageBase
from zopache.remote.mastodon.interfaces import IAddMastodonAccount
from zopache.remote.mastodon.remoteaccount import MastodonAccount
from zopache.ttw.mail import Notify
from zopache.business.exists import Duplicate
from zopache.ttw.htmlviews import AddCkHTMLBase
from zopache.pages.addpage import AddByTitleForm

@view_component
@name ('addMastodonAccount')
@target(IView)
@context(IPageBase)
class AddMsatodonAccount(AddByTitleForm):
     interface = IAddMastodonAccount
     title = "Add a Remote Mastodon Account"
     subTitle =""
     count = 0
     factory = MastodonAccount
     layoutName = "UserMenu"
     dataValidators = [Duplicate]
     def newName(self,data):
         return data['mastodonId'].strip()
     
     def newURL(self,baseURL):
        return baseURL + '/manage'




