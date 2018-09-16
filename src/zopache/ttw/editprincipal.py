from zope.interface import Interface
from zope.schema import TextLine , URI
from z3c.schema.email  import RFC822MailAddress as Email

#from cromlech.security import permissions
#from cromlech.security import Unauthorizedfrom zope.schema import TextLine,URI
from dolmen.forms.base import Actions

from zopache.core.viewdecorators import *

from zopache.core.breadcrumbs import parents
from zopache.core.viewdecorators import *
from zopache.crud.forms import EditForm
from .interfaces import IInternalPrincipal



class IGEdit(Interface):
    name = TextLine(
        title="Your Legal Name",
        description= "Your Legal Name, not publically visible",
        required = False)

    handle = TextLine(
        title="Handle ",
        description= "Your publically visible name.",
        required = True)
    """
    email = Email(
        title="Your Email Address",
        description ="We'll never share your email with anyone else.",
        required = True)
    """
    
    picture = URI(
        title = "Your Photo",
        description= "Ideally 80 x 80 px, but at least make it square.",
        required = False)
    
    homePage = URI(
        title = "Your Home Page",
        description= "For Chat.  Where people go to find out more about you. ",
        required = True)    
    
        
@form_component
@name (u'edit')
@permissions('Edit')    
@context(IInternalPrincipal)
@title("Edit")
class EditPrincipal(EditForm):
    title = 'Your Profile'
    interface = IGEdit
    fields = Fields(IGEdit)
    actions = Actions(formactions.Edit("Edit","Save"),
                          formactions.Cancel("Cancel","Cancel"))
    
    def acquireTitle(self):
        return 'Your Profile'

    def update(self):
        if not (self.request.principal in parents(self.context)):
                raise Unauthorized()
        return EditForm.update(self)
