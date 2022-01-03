from zope.interface import Interface
from zope import schema


from dolmen.forms.base.markers import HIDDEN

from zopache.core.viewdecorators import *
from zopache.crud.forms  import EditForm
from zopache.pages.interfaces import ICategory
from zopache.core.interfaces import ITreeSecurity

class IForm(Interface):
    html= schema.Text(
        title = 'HTML code',
        required = True,
        default = '',
    )
    
    json= schema.Text(
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

    def update (self):
        self.template = self.getProducts()['Templates']['EditorJS']['template']
        EditForm.update(self)
        self.fields["html"].mode = HIDDEN
        self.fields["json"].mode = HIDDEN    
    
    #def acquireTitle(self):
    #    return "Configure Server"


