from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema._field import Choice
from zope.schema import Text, Set, List


def possibleItems():
    terms = []
    #term = SimpleVocabulary.createTerm('None','None','None')
    #terms.append(term)    
    for item in [                'Manage',
                'AddContent',
                'EditContent',
                'Vote',
                 'Edit',                
                 'Add']:
        term = SimpleVocabulary.createTerm(item,item,item)
        terms.append(term)
    return SimpleVocabulary(terms)

class IPermissions(Interface):
         
    permissions = Set(
        value_type =Choice(source=possibleItems()),
        title="Permissions",
        description= "What is this user allowed to do",
        required = False)                

    

from zopache.core.viewdecorators import *
from zopache.ttw.interfaces import IInternalPrincipal
from zopache.crud.forms import EditForm

@form_component
@name (u'permissions')
@context(IInternalPrincipal)
@title("Edit Permissions")
@permissions('Manage')
class EditPermissions (EditForm):
    title = 'Edit User Permissions'
    suTitle = 'What is each user allowed to do.'
    interface = IPermissions
    fields = Fields(IPermissions)
    
    def url (self):
        return self.url() 
    
    def acquireTitle(self):
        return 'Edit Permissions'

    def postProcess(self):
        pass
