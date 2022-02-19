from zopache.core.viewdecorators import *
from zopache.json.editjsonschema import AddJson, EditJson
from zopache.core.interfaces import ITreeSecurity
from zopache.json.interfaces import INewsLetter

@form_component
@name ('ckedit')
@context(INewsLetter)
@implementer(ITreeSecurity)
class EditNewsLetter (EditJson):
    title = 'Edit this Newsletter.'
    subTitle = ''
    schemaName = "NewsletterSchema"

@form_component
@name ('aceedit')
@context(INewsLetter)
@implementer(ITreeSecurity)
class AceEditNewsletter (EditJson):
    title = 'Edit this Newsletter.'
    subTitle = ''
    schemaName = "NewsletterSchema"
    
