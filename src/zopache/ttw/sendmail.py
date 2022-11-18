from zope.interface import Interface
from zope import schema
from zopache.core.viewdecorators import *

from zopache.core.baseform import Form

class IMailForm(Interface):
    subject = schema.TextLine(
        title="Email Subject",
        description="What are you writing about",
        required=True,
        default=u'',
        )

    text= schema.Text(
        title = u'Source:',
        description = u'This is the text which defines the HTML.',
        required = False,
        default = u'',
    )
        
class SendMailForm(Form):    
    error = ''
    submissionError = ''
    label= ''
    interface = IMailForm
    title = "Contact The Editors"
    subTitle='At least two editors will receive this email.'
    @property
    def actions(self):
        return  Actions(
            SendMail("Add","Add"),
            Cancel("Cancel","Cancel"))
    
    @property
    def fields(self):
        return  Fields(self.interface)
