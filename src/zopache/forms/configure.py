import googlemaps

from zope.interface import Interface
from zope.schema._field import Choice
from zope.schema import TextLine, DottedName, Bool

from cromlech.browser.exceptions import HTTPFound
from cromlech.browser.interfaces import IPublicationRoot

from zopache.core.viewdecorators import *
from zopache.crud.forms import EditForm


class IForm(Interface):

    appName= TextLine(
        title = u'Domain.',
        description = "Name shown on Mastodon Oauth",
        required = False,
        missing_value = "",
    )

    domain= DottedName(
        title = u'Domain.',
        description = "Domain of this server",
        required = False,
        missing_value = "",
    )    

    diffDomain= DottedName(
        title = u'Diff Server',
        description = "With which you compare the ttw source code.",
        required = False,
        missing_value = "",
    )    

    subscribeSlug= TextLine(
        title = "Nefault Subscribe Page Name",
        description = "The Organization they shoudl subscribe to by default. ",
        required = False,
        default = '',
    )    

    localLogin = Bool(
        title = "Allow Local Logins?",
        description = "For security best to disable, and use Google OAuth login",
        required = False,
        default = True,
    )

    mastodonLogin = Bool(
        title = "Allow Mastodon Logins?",
        description = "Better than local Login or Google Oauth",
        required = False,
        default = False,
    )        

    mapBoxKey= TextLine(
        title = "MapBox Key",
        description = "Required For Maps",
        required = False,
        default = '',
    )
    geocondingKey= TextLine(
        title = "Google GeoCoding Key",
        description = "Converts an address into latitude and longitude.",
        required = False,
        default = '',
    )    

    youTubeKey= TextLine(
        title = "You Tube Key",
        description = "For Accessing Videos",
        required = False,
        default = '',
    )        
    
    twitterId= TextLine(
        title = 'Twitter Id',
        description = "Twitter Id.",
        required = False, 
        default = '',
    )
    instagramId= TextLine(
        title = u'Instagram Id',
        description = "How to reach you on Instagram.",
        required = False, 
        default = u'',
    )
    facebookId= TextLine(
        title = u'Facebook Id',
        description = "How to reach you on Facebook. .",
        required = False, 
        default = u'',
    )    
    basePath = TextLine(
        title = u'Base Path',
        description = "The base path for relative urls",
        required = False, 
        default = '/',
    )
    categoryName = TextLine(
        title = u'JSON Category Root',
        description = "What is the root of the Categories for the tree widget.",
        required = False, 
        default = u'',
    )

    mapName = TextLine(
        title = u'Map Name',
        description = "What is the url segment for the map for the tree widget.",
        required = False, 
        default = u'',
    )                     

    homePage= TextLine(
        title = "Home Page",
        description = "Shows a Logo.",
        required = False,
        default = u'',
    )

    templateRoot = TextLine(
        title = "Template Root",
        description = "What is the name of the page used for site templates?",
        required = False,
        default = '',
    )
    
@form_component
@name ('configure')
@context(IPublicationRoot)
@permissions('Manage')
class Configure (EditForm):
    title = 'Configure The Server'
    subTitle = "Various Parameters"
    interface = IForm
    fields = Fields(IForm)    
    
    def acquireTitle(self):
        return "Configure Server"


