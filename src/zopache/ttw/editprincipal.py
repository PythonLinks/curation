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
from zopache.crud.forms import BaseEditForm
from zopache.ttw.interfaces import IInternalPrincipal, ISupport
from zopache.ttw.treewidget import TreeField
from zopache.pages.interfaces import IPage
from zopache.core.interfaces import ITreeSecurity



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
    description= schema.Text(
        title = 'Description',
        description = """A brief introduction for this person.  """,
        required = False,
        default = u'',
    )

    remoteURL= schema.URI(
        title = 'URL',
        description = """A URL for this person. 
             Please include 'https://'""",
        required = False,
        missing_value = "",
    )
    
    source= schema.Text(
        title = u'Content',
        description = u'This is the main content for this page',
        required = False,
        default = u'',
    )


    """    
    professionalURL = TextLine(
        title="Your Proessinal URL",
        description="Your professional website, or Linkedin page.",
        required=False,
        default=u'',
        missing_value=u'')


    

    data = FileField( title ="Or Post Your CV or Resume",
                      description = "It is only shown to those whom you allow to see it..",
                      required = True 
    )
    
    who = Set(
        value_type =Choice(source=possibleItems()),
        title="View Permissions",
        description= "Who is allowed to see your information?",
        required = False)                

    where=TreeField(
        title="Location Permissions",
        description= "Where can people see your information?",
        required = False,
    )
    """

@form_component
#@name (u'edit')
@context(IInternalPrincipal)
class EditPrincipal(BaseEditForm):
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


@form_component
@name (u'aceedit')
@context(IInternalPrincipal)
@implementer(ITreeSecurity)
class AceEditPrincipal(AceEdit):
    title = 'Ace Edit Your Profile'
    interface = IEdit
    @property
    def fields(self):
        return  Fields(self.interface)
    
@form_component
@name (u'ckedit')
@context(IInternalPrincipal)
@implementer(ITreeSecurity)
class CkEditPrincipal(CkEdit):
    title = 'CkEdit Your Profile'
    interface = IEdit
    @property
    def fields(self):
        return  Fields(self.interface)
    
@form_component
#@name (u'support')
@context(IInternalPrincipal)
@title("Edit")
class EditSupport (EditPrincipal):
    interface = IEdit

    preamble = """ If you like this website, please support the business 
                   model by checkng one of the following two boxes. """
    postamble = """What is 
                   the business model?  I am a recruiter.  Instead of spamming 
                   people, I publish good information, earn their respect, 
                   and if I see a job they would like, I recruit them. By 
                   checking one of the GDPR boxes above you give me 
                   permission to do so.  
                   In practice I already have GDPR permission for over 
                   200 candidates, what I am short on is clients.    
               """
    def acquireTitle(self):
        return 'GDPR Permissions'
    
    subTitle = " "

    actions = Actions(formactions.SaveAndViewURL("Save","Save"),
                          formactions.Cancel("Cancel","Cancel"))    

    def newURL(self,new):
        if self.context.hirePermission:
            newURL = '/' + self.context.__name__ + "/edit"
        else:
            newURL = '/'
        return newURL
