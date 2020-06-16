#ADD LINK
from zopache.core.viewdecorators import *
from zopache.core.interfaces import ITreeSecurity
from zopache.crud.addbyurl import AddByURLForm

#The Classes to Add
from zopache.remote.rss import RSS
from zopache.business.company import Organization
from zopache.pages.page import Link
from zopache.pages.interfaces import IPage

@view_component
@name('addByURL')
@target(IView)
@context(IPage)
@implementer(ITreeSecurity)
class AddLinkByURL(AddByURLForm):
    title = "Add a Link"
    def newURL(self,base):
        return base + '/addLink'

@view_component
@name('addOrganizationByURL')
@target(IView)
@context(IPage)
class AddOrganizationByURL(AddByURLForm):
    allowAnonymous = True
    title = "Add an Organizatino"
    def newURL(self,base):
        return base + '/addOrganization'


@view_component
@name('addNewsSiteByURL')
@target(IView)
@context(IPage)
class AddRSSByURL(AddByURLForm):
    title = "Add a News Site"
    subTitle = "Not an article, just the home page. "
    def newURL(self,base):
        return base + '/addRSS'
    
@view_component
@name('addPoliticianByURL')
@target(IView)
@context(IPage)
class AddPoliticianByURL(AddByURLForm):
    allowAnonymous = True
    title = "Add a News Site"
    subTitle = "Not an article, just the home page. "
    def newURL(self,base):
        return base + '/addPolitician'        
