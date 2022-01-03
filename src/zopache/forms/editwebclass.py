from zope.interface import Interface
from zope.schema import TextLine

from zopache.core.viewdecorators import *
from zopache.crud.forms import EditForm
from zopache.pages.interfaces import IPage

class IClass(Interface):

    webClass= TextLine(
        title = u'WebClass.',
        description = u'Defines the source of html, css, javascript aand images',
        required = True,
        default = u'',
    )         

@form_component
@name ('editWebClass')
@context(IPage)
@permissions('Manage')
class EditWebClass (EditForm):
    title = 'Edit the WebClass.'
    subTitle = 'This is used to change the layout of this object.'
    interface = IClass
    fields = Fields(IClass)
    
    def acquireTitle(self):
        return 'Edit' + self.context.title + "'s Web Class "


