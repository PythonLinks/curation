import googlemaps

from zope.interface import Interface
from zope.schema._field import Choice
from zope.schema import TextLine, DottedName, Bool

from cromlech.browser.exceptions import HTTPFound
from cromlech.browser.interfaces import IPublicationRoot

from zopache.core.viewdecorators import *
from zopache.crud.forms import EditForm
from zopache.ttw.interfaces import IInternalPrincipal
from zopache.remote.mastodon.basebot import BaseBot

class IForm(Interface):

    accessToken= TextLine(
        title = "Mastodon Access Token",
        description = "Used by the api.",
        required = False,
        default = '',
    )    

@form_component
@name ('mastodon')
@context(IInternalPrincipal)
@permissions('Manage')
class Configure (EditForm,BaseBot):
    title = 'Mastodon Configurtion'
    subTitle = "Various Parameters"
    interface = IForm
    fields = Fields(IForm)    
    description = ""
    #@property
    #def description(self):
    #    desciption = '''In order to allow you to access Mastodon from this 
    #            site, an accessToken is needed.  <a href=" '''
    #    description += ""
    #    description +='''
    #    ">Please click here</a>, authorize this application, 
    #    and then manually copy the authorization token back into the form 
    #    below.'''
 
    def acquireTitle(self):
        return "Configure Server"


