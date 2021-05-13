from slugify import slugify

from zopache.crud.addbyurl import  AddByURLForm
from zopache.crud.forms import AddByTitleForm
from zopache.core.interfaces import ITreeSecurity,IUserSecurity
from zopache.core.viewdecorators import *
from zopache.pages.interfaces import IPageBase, IPage
from zopache.remote.rss import IRSS, IJustRSS, IRSSBase, RSS, JustRSS
from zopache.remote.rssarticle import IRSSArticle, RSSArticle
from zopache.core.page import Page
from zopache.ttw.mail import Notify
from BTrees.OOBTree import OOBTree
from dolmen.container import IBTreeContainer
from zopache.business.exists import Duplicate
from zopache.remote.rsscategory import RSSCategory, IRSSCategory

@view_component
@name('addRSS')
@target(IView)
@context(IPage)
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddRSS(AddByTitleForm,Notify):
     interface = IRSS
     title = "Add an RSS Feed"
     subTitle =""
     count = 0
     factory = RSS
     layoutName = "UserMenu"
     dataValidators = [Duplicate]
     
     def newURL(self,baseURL):
        return baseURL + '/manage'



@view_component
@name('addRSSCategory')
@target(IView)
@context(IPageBase)
@implementer(ITreeSecurity)
class AddRSSCategory(AddByTitleForm,Notify):
     interface = IRSSCategory
     title = "Add an RSS Category"
     subTitle =""
     count = 0
     factory = RSSCategory
     layoutName = "UserMenu"
     dataValidators = [Duplicate]
        
@view_component
@name('addJustRSS')
@target(IView)
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddJustRSS(AddByTitleForm,Notify):
     interface = IJustRSS
     title = "Just add an RSS Feed"
     subTitle =""
     count = 0
     factory = JustRSS
     layoutName = "UserMenu"
     dataValidators = [Duplicate]
     
     def newURL(self,baseURL):
        return baseURL + '/manage'   
               
from zopache.core.baseform import Form
from zope.interface import Interface

""""
No longer used.  WAS USED FOR some strANge stuff. y

@view_component
@name('ckedit')
@target(IView)
@context(IRSS)
@implementer(ITreeSecurity)
class EditRSS(E):
    title = "Update an RSS Feed"
    subtitle = "All feeds will be fetched  again. "
    count = 0
    schemaName = "rssSchema"     
    def update(self):
        self.status='RSS Was updated'
        Form.update(self)
"""

@view_component
@name('addRSSByURL')
@target(IView)
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class AddRSSByURL(AddByURLForm,Notify):
    factory = RSS
    def newURL(self,baseuRL):
        breakpoint()
        return baseURL + "/addRSS" 
