import googlemaps

from zope.interface import Interface
from zope.schema._field import Choice
from zope.schema import TextLine, DottedName, Bool

from cromlech.browser.exceptions import HTTPFound
from cromlech.browser.interfaces import IPublicationRoot

from zopache.core.viewdecorators import *
from zopache.crud.forms import EditForm
from zopache.pages.interfaces import IRootPage

class IForm(Interface):

    domain= DottedName(
        title = u'Domain.',
        description = "Domain of this server",
        required = False,
    )

    googleClientId= TextLine(
        title = "Google Oauth Client Id",
        description = "For Logins",
        required = False,
        default = u'',
    )

    mapBoxKey= TextLine(
        title = "MapBox Key",
        description = "Required For Maps",
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

    rssRoot = TextLine(
        title = u'RSS Root',
        description = "What is the root of the RSS Tree.",
        required = False, 
        default = u'',
    )                 

    homePage= TextLine(
        title = "Home Page",
        description = "Shows a Logo.",
        required = False,
        default = u'',
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


