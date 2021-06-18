#ADD LINK
from dolmen.forms.base import Action, Actions,SuccessMarker
from zopache.core.viewdecorators import *
from zopache.core.interfaces import ITreeSecurity
from zopache.crud.addbyurl import AddByURLForm
from zopache.crud.actions import Cancel
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
    title = "Add a Link By URL"
    addSlug = "addLink"

from zopache.crud.addbyurl import AddFeedByURLAction        
    
@view_component
@name('addRSSByURL')
@target(IView)
@context(IPage)
@permissions('Manage')
class AddRssByURLForm(AddByURLForm):
    addSlug = "addRSS"
    title = "Add an RSS Feed"
    datavalidators = []
    def addUnauthorizedActions(self):   
        actions = Actions(
                   AddFeedByURLAction("Add"),
                   Cancel("Cancel"))
        self.actions= actions    


    
@view_component
@name('addOrganizationByURL')
@target(IView)
@context(IPage)
class AddOrganizationByURL(AddByURLForm):
    allowAnonymous = True
    title = "Add an Organization By URL"
    addSlug = 'addOrganization'

    
@view_component
@name('addPoliticianByURL')
@target(IView)
@context(IPage)
class AddPoliticianByURL(AddByURLForm):
    allowAnonymous = True
    title = "Add a Politician By URL "
    subTitle = "Not an article, just the home page. "
    addSlug = 'addPolitician'        
