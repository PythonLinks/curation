from zope import schema
from pyramid_mailer.mailer import Mailer

from zopache.core.viewdecorators import *
from zopache.core import Leaf
from zopache.crud.interfaces import ILeaf
from zopache.pages.interfaces import IRootPage
from zopache.crud.forms import AddForm, EditForm

class IMailHost(ILeaf):
    """Basic Mail CRUD"""
    host = schema.TextLine(
        title = u'Host Name',
        description = u'Which Mail Server are you using?',
        required = True,
    )
    
    port = schema.Int(
        title = u'Port',
        description = u'MailHost Port Number',
        required = True,
        default = 25,
    )

    username= schema.TextLine(
        title = u'username',
        description = u'Who is the user sending the email',
        required = True,
    )

    password= schema.Password(
        title = 'password',
        description = 'The password used to send mail.',
        required = True,
    )    
    

@implementer (IMailHost)
class MailHost(Mailer,Leaf):
    def __init__(self):
        Leaf.__init__(self)
        Mailer.__init__(self)        
    
@form_component
@name('addMailHost')
@context(IRootPage)
@permissions('Manage')
class AddMailHost(AddForm):
    subTitle='Add a MailHost'
    interface = IMailHost
    ignoreContent = True
    factory=MailHost
    def newName(self,data):
        return "MailHost"
    
#HERE IS THE  EDIT FORM
@form_component
@context(IMailHost)
@name("edit")
@permissions('Manage')
class EditMailHost(EditForm):
    subTitle='Edit the MailHost Object'    
