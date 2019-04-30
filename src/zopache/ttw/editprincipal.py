from zope.interface import Interface
from zope.schema import TextLine , URI, Password
from z3c.schema.email  import RFC822MailAddress as Email

#from cromlech.security import permissions
from cromlech.security import Unauthorized
from zope.schema import TextLine,URI
from dolmen.forms.base import Actions
from cromlech.file import FileField

from zopache.core.viewdecorators import *
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema._field import Choice
from zope.schema import Text, Set, List
from zopache.core.breadcrumbs import parents
from zopache.core.viewdecorators import *
from zopache.crud.forms import BaseEditForm
from zopache.ttw.interfaces import IInternalPrincipal
from zopache.ttw.treewidget import TreeField

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

    data = FileField( title ="Your CV or Resume",
                      description = "It is only shown to those whom you allow to see it..",
                      required = False 
    )
    
    who = Set(
        value_type =Choice(source=possibleItems()),
        title="View Permissions",
        description= """Who is allowed to see 
                         your information?""",
        required = False)                
    """
    where=TreeField(
        title="Location Permissions",
        description= "Where can people see your information?",
        required = False,
    )
    """
    
@form_component
@name (u'edit')
@context(IInternalPrincipal)
@title("Edit")
class EditPrincipal(BaseEditForm):
    title = 'Your Profile'
    interface = IEdit
    fields = Fields(IEdit)
    actions = Actions(formactions.SaveAndRoot("Save","Save"),
                          formactions.Cancel("Cancel","Cancel"))
    def acquireTitle(self):
        return 'Your Profile'


    def update(self):
        if not (self.request.principal is self.context):
                raise Unauthorized()
        return BaseEditForm.update(self)
