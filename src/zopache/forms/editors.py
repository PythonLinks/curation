from zope.interface import Interface
from zope import schema
from zopache.core.viewdecorators import *
from zopache.crud.forms import EditForm
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from zope.interface import directlyProvides
from zopache.core.getroot import getPrincipalFolder

def possibleEditors(context):
    people = getPrincipalFolder(context)
    terms = []
    term = SimpleVocabulary.createTerm('None','None','None')
    terms.append(term)    
    for key, principal  in people.items():
        email =  principal.email
        term = SimpleVocabulary.createTerm(key, key, email)
        terms.append(term)
    return SimpleVocabulary(terms)

directlyProvides(possibleEditors, IContextSourceBinder)


#THIS ONE WORKS, BUT BOY IS IT UGLY.

class IEditors(Interface):
     editors = schema.Set(
         title=u"Editor",
        value_type=schema.Choice(source=possibleEditors),
        required=False,
    )

"""
class IEditors(Interface):
     editors = schema.Choice(
         title=u"Editor",
         source = possibleEditors,
        required=False,
    )
"""     

    
@form_component
@name (u'editors')
@permissions('Manage')    
@context(Interface)
@title("Assign Editors")
class EditEditors(EditForm):
    title = 'Assign Editors'
    interface = IEditors
    fields = Fields(IEditors)
    ignoreContent = False
  #  mode = 'multiselect'
 
    #def update(self):
    #    editorsField=self.fields['editors']
    #    editorsField.

