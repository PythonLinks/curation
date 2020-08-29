from zope.interface import Interface
from zope.schema import TextLine , URI, Password
from zope import schema
from z3c.schema.email  import RFC822MailAddress as Email

#from cromlech.security import permissions
from cromlech.security import Unauthorized
from zope.schema import TextLine,URI
from dolmen.forms.base import Actions
from cromlech.file import FileField

from zopache.ttw.htmlviews import AceEdit, CkEdit
from zopache.core.viewdecorators import *
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema._field import Choice
from zope.schema import Text, Set, List
from zopache.core.viewdecorators import *
from zopache.crud.forms import EditForm
from zopache.ttw.interfaces import IInternalPrincipal, ISupport
from zopache.ttw.treewidget import TreeField
from zopache.pages.interfaces import IPage
from zopache.core.interfaces import ITreeSecurity
from zopache.application.choices import fromList


def possibleItems():
    terms = []
    #term = SimpleVocabulary.createTerm('None','None','None')
    #terms.append(term)    
    items = [
            ("Hiring Managers","managers"),
            ("Christopher Lozinski","lozinski"),
            ("Technical Staff","technicalStaff"),
            ("Internal Recruiters","internalRecruiters"),
            ("External Recruiters","externalRecruiters")
    ]
    for item in items:
        term = SimpleVocabulary.createTerm(
                    item[1],item[1],item[0])
        terms.append(term)
    return SimpleVocabulary(terms)


class IEdit(Interface):
    publicName= schema.TextLine(
        title = u'Your Public Name(optional)',
        description = 'Privacy is important.',
        required = False,
        default = '',
    )
    
    description= schema.Text(
        title = 'Description',
        description = """A brief introduction for this person.  """,
        required = False,
        default = u'',
    )
    preferredChannel = schema.Choice(
        source = fromList(['Phone Call',
                                                      'SMS',
                                                      'Email',                                                                       'Twitter',
                                                      'Facebook',
                                                      'Signal',
                                                      'Telegram']),
        title="Preferred Contact Channel",
        description= "How do you like to be contacted?",
        required = False,)


    twitterId= schema.TextLine(
        title = u'TwitterId (Optional)',
        description = u'Do not include the @ symbol.',
        required = False,
        default = '',
    )

    facebookId= schema.TextLine(
        title = 'Facebook Page (Optional)',
        description = "Please include 'https://'.",
        required = False,
        default = '',
    )

    phoneNumber= schema.TextLine(
        title = 'Phone Number(Optional)',
        description = "This one should be obvious",
        required = False,
        default = '',
    )

    preferredmail= Email(
        title = u'Email Address (Optional)',
        description = u'Can they email you? Make sure there are no spaces. ',
        required = False,
        missing_value = '',
    )
    
    remoteURL= schema.URI(
        title = 'URL',
        description = """A URL for this person. 
             Please include 'https://'""",
        required = False,
        missing_value = "",
    )


@form_component
@name (u'edit')
@context(IInternalPrincipal)
class EditPrincipal(EditForm):
    title = 'Your Profile'
    interface = IEdit
    actions = Actions(formactions.SaveAndRoot("Save","Save"),
                          formactions.Cancel("Cancel","Cancel"))

    def acquireTitle(self):
        return 'Your Profile'

    def update(self):
        if  (self.request.principal is self.context):
           return
        if 'Manage' in self.request.principal.permissions:
           return 
        raise Unauthorized()

    @property
    def fields(self):
        return  Fields(self.interface)
