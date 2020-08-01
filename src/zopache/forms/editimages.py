from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema._field import Choice
from zope.schema import Text, Set, List
from zopache.application.choices import fromList
from zopache.ttw.interfaces import IImage
from zopache.core.interfaces import ITreeSecurity
from zopache.core.viewdecorators import *
from zopache.crud.forms import EditForm

@form_component
@name ('edit')
@context(IImage)
@implementer (ITreeSecurity)
class EditImage (EditForm):
    title = 'Edit an Image'
    suTitle = 'Set some info'
    interface = IImage
    fields = Fields(IImage)
        
    def acquireTitle(self):
        return 'Edit Image'

