import googlemaps

from zope.interface import Interface
from zope.schema._field import Choice
from zope.schema import TextLine, Text

from cromlech.browser.exceptions import HTTPFound

from zopache.ttw.mail import Notify
from zopache.core.viewdecorators import *
from zopache.crud.forms import EditForm
from zopache.pages.interfaces import IPage

class IClass(Interface):

    newsTitle= TextLine(
        title = 'News Title.',
        description = 'What is this newsletter called',
        required = True,
        default = '',
    )

    preAmble = Text(
        title = 'News PreAmble.',
        required = False,
        default = '',
    )             

@form_component
@name ('sendNews')
@context(IPage)
@permissions('Manage')
class SendNews (Notify,EditForm):
    title = 'Send one Newsletter.'
    interface = IClass
    fields = Fields(IClass)
    
    def __init__(self,context,request):
        Notify.__init__(self)
        EditForm.__init__(self,context,request)
        
    def acquireTitle(self):
        return 'Edit' + self.context.title + "'s Web Class "

    def postProcess(self,view = None):
        self.sendMeANewsletter()
        del self.context.newsTitle
        del self.context.preAmble


@form_component
@name ('broadcast')
@context(IPage)
@permissions('Manage')
class Broadcast (Notify,EditForm):
    title = 'Broadcast the News.'
    interface = IClass
    fields = Fields(IClass)
    
    def __init__(self):
        Notify.__init__(self)
        EditForm.__init__(self)
        
    def acquireTitle(self):
        return 'Edit' + self.context.title + "'s Web Class "

    def postProcess(self,view = None):
        self.broadcastNews()
        del self.context.newsTitle
        del self.context.preAmble
        
