from zope.interface import Interface
from zope.schema import Bool
from zope.cachedescriptors.property import CachedProperty
from zope.schema import Text, TextLine, Choice, Bool

import crom
from dolmen.forms.base import Actions
from dolmen.forms.base import Action, SuccessMarker
from dolmen.forms.base import Actions

from zopache.core.breadcrumbs import parents
from zopache.core.viewdecorators import *
from zopache.crud.forms import  EditForm
from cromdemo.interfaces import ITab
from .interfaces import IInternalPrincipal
from zopache.crud.actions import Update

class ISpeakerQuestionaire(Interface):    
    speakerPermission = Bool(
        title = "Speaker Permission"  ,
        description = """I give permision to process my professional  information for the purpose of inviting me to speak at meetups and conferences in the places I list below. """,
        required = True,
        default = False)

    whereCanYouSpeak  = Text(
        title="Where can you speak?",
        required=True,
        default=u'',
        missing_value=u'')
    
    phone  = TextLine(
        title="Your Phone NUmber",
        description = """Your phone number will not be given to anyone else without your explicit permission.""",
        required=True,
        default=u'',
        missing_value=u'')

    needExpenses = Bool(
        title = "Need Expenses?",
        description = "Check here if you would need your travel expenses reimbursed.",
        required = False,
        default = False)


    needHelp = Bool(
        title = "Need Help?",
        description = "Check here if you would want some help with your presentation. In general the organizers are very supportive.",
        required = False,
        default = False)
    

class Done (Update):
    def newURL(self,arg):
        return ('/')

class NoThanks (Action):
    def __call__(self, form):
        url= '/'
        return SuccessMarker('Done', True, url=url,code=307)

@form_component
@name (u'meetupspeaker')
@context(IInternalPrincipal)
@permissions('Edit')
@title("Meetup Speaker Permissions")
class RegisterSpeaker(EditForm):
    """ Speaker Permissions
    """
    title='PythonLinks.info'
    subTitle='Become a Speaker'
    fields = Fields(ISpeakerQuestionaire)
    submissionError = []

    
    def updateWidgets(self):
        EditForm.updateWidgets(self)
        widgets = self.widgetDictionary()
        item = item2 = widgets['form-field-speakerPermission']
        item.defaultHtmlClass = ['field']
        item = widgets['form-field-whereCanYouSpeak']
        item._htmlAttributes['rows']=3
        item._htmlAttributes['placeholder']="""Where would you be willing to speak?  Anywhere in Europe?  Anywhere in your country?  Only in the following ciites?  Only at the following meetups or conferences?"""
        item = widgets['form-field-phone']        
        item._htmlAttributes['placeholder']="Please include the country code"
        print(item.htmlAttributes())

    def breadcrumbs(self):
        return ""
    
    def update(self):
        if not (self.request.principal in parents(self.context) or
                self.request.principal.__name__=='lozinski'):
                raise Unauthorized()        
        root = self.getRoot()
        self.template = root['Products']['Templates']['SpeakerPermissions']
        
    @CachedProperty
    def actions(self):
        return Actions(Done("Agreed",  "Agreed"),
                       NoThanks("No Thanks",  "No Thanks"))
	      
