from zope.interface import Interface
from zope import schema
from dolmen.container import IBTreeContainer

from zopache.core.viewdecorators import *
from zopache.crud.forms import EditForm
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from zope.interface import directlyProvides
from zopache.core.getroot import getPrincipalFolder
from zopache.core.interfaces import ITreeSecurity

def possibleEditors(context):
    people = getPrincipalFolder(context)
    terms = []
    term = SimpleVocabulary.createTerm('None','None','None')
    terms.append(term)    
    for key, principal  in people.items():
        title =  principal.title
        term = SimpleVocabulary.createTerm(key, key, title)
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

    
@form_component
@name (u'editors')
@context(IBTreeContainer)
@implementer(ITreeSecurity)
class EditEditors(EditForm):
    title = 'Assign Editors2'
    interface = IEditors
    fields = Fields(IEditors)
    ignoreContent = False
    #  mode = 'multiselect'
  
    def update(self):
      EditForm.update(self)  
      self.template = self.getTemplates()['Security']
           

