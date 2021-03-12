from slugify import slugify


from cromlech.security import Unauthorized
from zopache.crud.addbyurl import  AddByURLForm
from zopache.crud.forms import AddByTitleForm
from zopache.core.interfaces import ITreeSecurity,IUserSecurity
from zopache.core.viewdecorators import *
from zopache.pages.interfaces import IPage
from zopache.ttw.interfaces import IContainer
from zopache.remote.rss import IRSS,  IRSSPage, RSS
from zopache.remote.rssarticle import IRSSArticle, RSSArticle
from zopache.core.breadcrumbs import Breadcrumbs
from zopache.core import View
from zopache.core.page import Page
   
from zopache.crud.forms import AddByNameForm
from zopache.ttw.mail import Notify
from zopache.crud.forms import BaseEditForm
import zopache
from zopache.crud.forms import BaseEditForm
from BTrees.OOBTree import OOBTree
from dolmen.container import IBTreeContainer
from zopache.business.exists import Duplicate

@view_component
@name('addRSS')
@target(IView)
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
     
     def __init__(self):
        Notify.__init__(self)
        AddByTitleForm.__init__(self)
        
     def newURL(self,baseURL):
        return baseURL + '/manage'
            
   
from zopache.core.baseform import Form
from zope.interface import Interface
@view_component
@name('updateRSS')
@target(IView)
@context(IRSS)
@implementer(ITreeSecurity)
class UpdateRSS(Form):
     interface = Interface
     title = "Update an RSS Feed"
     subTitle ="Download new Articles Category"
     count = 0
     layoutName = "UserMenu"
     def update(self):
        self.status='RSS Was updated'
        Form.update(self)
        
@form_component
@name ('edit')
@context(IRSS)
@implementer(IUserSecurity)
class EditRSS(BaseEditForm):
    pass

from zopache.ttw.htmlviews import CkEdit
@form_component
@name ('edit')
@context(IRSSArticle)
@implementer(IUserSecurity)
class EditRSSLink(CkEdit):
    pass

#@view_component
#@name('addNewsSite')
#@target(IView)
#@context(IContainer)
#@implementer(ITreeSecurity)
#class AddRSSByURL(AddByURLForm,Notify,Base):
#     factory = RSS
              
