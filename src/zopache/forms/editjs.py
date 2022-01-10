import json
from zope.interface import Interface
from zope import schema

from zopache.core.viewdecorators import *
from zopache.crud.forms  import EditForm
from zopache.pages.interfaces import ICategory
from zopache.core.interfaces import ITreeSecurity

class IForm(Interface):
    title= schema.TextLine(
        title = 'Article Title',
        required = True,
    )

    html= schema.Text(
        title = 'HTML code',
        required = False,
        default = '',
    )    
    
    source= schema.Text(
        title = 'Json Data',
        required = True,
        default = '{}',
    )    
    
    articleApproved = schema.Bool(
        title = "Can this article be published?",
        required = False,
        default = False)
    
@form_component
@name ('editjs')
@context(ICategory)
@implementer(ITreeSecurity)
class EditorJS(EditForm):
    title = 'Curated Content Editor'
    subTitle = ""
    interface = IForm
    fields = Fields(IForm)

    def preProcess(self):
        pass
    
    def postProcess(self, view = None):
        source = json.loads(self.context.source)
        self.context.source = json.dumps(source,indent = 2)
    
    def update (self):
        self.template = self.getProducts()['Templates']['EditorJS']['template']
        EditForm.update(self)
        #NOT NEEDED, USING A TEMPLATE
        #self.fields["html"].mode = HIDDEN
        #self.fields["source"].mode = HIDDEN    
    
    #def acquireTitle(self):
    #    return "Configure Server"


