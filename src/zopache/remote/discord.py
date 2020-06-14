from zope import schema

from dolmen.forms.base.markers import HIDDEN

from zopache.ttw.treewidget import TreeField
from zopache.pages.page import Link
from zopache.crud.actions import AddByTitleToTreeAndView
from zopache.core.viewdecorators import *
from zopache.pages.interfaces import IPage
from zopache.pages.addanonymous import AddAnonymousToTree

class IDiscordForm(Interface):
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
               default = u'',
               )

    source= schema.Text(
        title = u'More Content',
        description = u'if the description is too long, please move part of it it here.',
        required = False,
        default = u'',
    )
    
    categoryName=TreeField(
           title="Category",
           description= """The category specifies where in the subject 
taxonomy this link will be placed.  You are encouraged to place it 
in a leaf of the tree.""",
           required = True,
            )
    
    
    discordGuildId = schema.TextLine(
        title = 'The Discord Server',
        required = True,
    )
    
    discordChannelId = schema.TextLine(
        title = 'The Discord Channel',
        required = True,
    )
    
    discordUserName = schema.TextLine(
        title = u'The Discord User Name',
        required = True,
    )
    discordUserId = schema.TextLine(
        title = u'The Discord User Id',
        required = True,
    )      

    

from dolmen.forms.base.widgets import Widgets    
@view_component
@name('fromDiscord')
@target(IView)
@context(IPage)
class AddLinkFromDiscord(AddAnonymousToTree):
    ignoreRequest = False
    layoutName = "UserMenu"    
    interface = IDiscordForm 
    title = "Add a Link"
    factory = Link
        
    def updateWidgets(self):
        AddAnonymousToTree.updateWidgets(self)
        widgets = self.widgetDictionary()
        style = "display:none;"

        widgets['form-field-discordGuildId']._htmlAttributes['style'] = style
        widgets['form-field-discordUserId']._htmlAttributes['style'] = style
        widgets['form-field-discordUserName']._htmlAttributes['style'] = style
        widgets['form-field-discordChannelId']._htmlAttributes['style'] = style
        widgets['form-field-discordGuildId'].component.mode = HIDDEN
        widgets['form-field-discordUserId'].component.mode = HIDDEN
        widgets['form-field-discordUserName'].component.mode = HIDDEN
        widgets['form-field-discordChannelId'].component.mode = HIDDEN        

        
    def postAddProcess(self, view=None):
        #del self.new.discordUserId
        #del self.new.discordUserId        
        #del self.new.discordGuild
        #del self.new.discordChannel        
        AddAnonymousToTree.postAddProcess(self,view=self)

