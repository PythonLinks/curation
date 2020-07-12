from zope import schema

from dolmen.forms.base.markers import HIDDEN

from zopache.ttw.treewidget import TreeField
from zopache.pages.page import Link
from zopache.crud.actions import AddByTitleToTreeAndView
from zopache.core.viewdecorators import *
from zopache.pages.interfaces import IPage
from zopache.pages.addanonymous import AddToTree, AddAnonymousPage
from zopache.remote.validatediscord import ValidateDiscord

class IBaseForm(Interface):
    title = schema.TextLine(
        title = 'Page Title',
        description = 'Please choose an approprite title for the remote page.',
        required = True,
    )

    remoteURL= schema.URI(
        title = 'URL',
        description = 'The url of the remote web page.',
        required = True,
    )
    
    description = schema.Text(
               title = "Page Summary",
               description = """A brief introduction of this page.  
                        You are encouraged to edit this 
               part to make it more relevant.""",
               required = False,
               default = '',
               )

    source= schema.Text(
        title = u'More Content',
        description = """if the description is too long, 
please move part of it here.""",
        required = False,
        default = '',
    )
    
    webApproved = schema.Bool(
        title = "Approved for publication on the web.",
        required = False,
        default = False)
    
    discordGuildId = schema.Int(
        title = 'The Discord ServerId',
        required = True,
    )
    
    discordChannelId = schema.Int(
        title = 'The Discord Channel Id',
        required = True,
    )
    
    discordUserName = schema.TextLine(
        title = u'The Discord User Name',
        required = True,
    )
    discordUserId = schema.Int(
        title = u'The Discord User Id',
        required = True,
    )
    
    discordUserDiscriminator = schema.Int(
        title = u'The Discord User Discriminator',
        required = True,
    )          

    
class ILinkForm(IBaseForm):    
    categoryName=TreeField(
           title="Category",
           description= """The category specifies where in the subject 
taxonomy this link will be placed.  You are encouraged to place it 
in a leaf of the tree.""",
           required = True,
            )
    
class IOrganizationForm(IBaseForm):
    pass

class INewsForm(IBaseForm):
    pass

from dolmen.forms.base.widgets import Widgets
from zopache.remote.validatediscord import ValidateDiscord
from dolmen.view import make_view_response
from dolmen.forms.base import Action, SuccessMarker
class BaseClass(AddAnonymousPage):
    make_response = make_view_response
    submissionErrors = []
    dataValidators = [ValidateDiscord]
    ignoreRequest = False
    layoutName = "UserMenu"
    
    def getReturn(self,url):
        return SuccessMarker('Added', True)
        
    def updateWidgets(self):
        AddAnonymousPage.updateWidgets(self)

    #Have to subclass, because addAnonymous sets
    #webApproved to be False
    def postAddProcess(self,view = None):
        self.new.postAddProcess (view = self)
        self.notifyAdminsNewPage()
        

@view_component
@name('fromDiscord')
@target(IView)
@context(IPage)
class AddLinkFromDiscord(AddToTree,BaseClass):
    allowAnonymous = True    
    interface = ILinkForm
    title = "Add a Link"
    factory = Link
    def render(self):
        response = ""
        #for item in self.formErrors:
        #       response += item.title + " "
        #response += item.identifier
        #for item in self.submissionError:
        #       response += item.title 
        #       response += item.identifier 
        for item in self.errors:
                 response +=  item.title
                 response +=  " " + item.identifier
        for widget in self.fieldWidgets:
            if hasattr (widget, 'err') and widget.err:
               response += widget.title
               response += widget.identifier               
        if response and response != "form":
               return response
           
        if hasattr(self,'new'):
           url = self.secureShortURL(context=self.new)
           url = self.shortenURL(url)
           message = f" Here is your new posting <{url}>."
           return "Success" + message
        return "Error, nothing created!"
    
from zopache.business.company import Organization        
@view_component
@name('addOrganizationFromDiscord')
@target(IView)
@context(IPage)
class AddOrganizationFromDiscord(BaseClass):        
    interface = IOrganizationForm
    title = "Add an Organization"
    factory = Organization

from zopache.remote.rss import RSS    
@view_component
@name('addNewsSiteFromDiscord')
@target(IView)
@context(IPage)
class AddNewsSiteDiscord(BaseClass):        
    interface = INewsForm
    title = "Add a News Site"
    factory = RSS
