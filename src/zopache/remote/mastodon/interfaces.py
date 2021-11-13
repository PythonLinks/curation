from zope.interface import Interface
from zope import schema
from z3c.schema.email  import RFC822MailAddress as Email
from zope.schema.vocabulary import SimpleVocabulary,SimpleTerm

from zopache.crud.interfaces import IContainer

class IServer(IContainer):

    """Basic Mastodon Server Crud"""
    
    title = schema.TextLine(
        title = u'Page Name',
        description = u'Describe this page.',
        required = True,
    )
    
    mastodonDomain = schema.DottedName(
        title = u'Host Name',
        description = u'Which Server is this?',
        required = True,
    )
    
    clientKey= schema.TextLine(
        title = "Mastodon Client Key",
        required = False,
        default = '',
    )

    clientSecret= schema.TextLine(
        title = "Mastodon Client Secret",
        required = False,
        default = '',
    )
    
    #Mastodon Access token
    accessToken= schema.TextLine(
        title = "Mastodon Access Token",
        description = "Used by the api.",
        required = False,
        default = '',
    )    
    userName= schema.TextLine(
        title = 'User Name',
        description = 'Who is the user for this account',
        required = True,
    )
    password= schema.TextLine(
        title = 'User Password',
        description = 'The password used to send mail.',
        required = True,
    )


class IRegister(Interface):
    mastodonDomain = schema.DottedName(
        title = "Mastodon Server",
        readonly = True,
     )   
    userName = schema.TextLine(
        readonly = True,
        title = "User Name"         
    )
        
    displayName = schema.TextLine(
        readonly = True,
        title = "Display Name"         
    )    

    accessToken= schema.Text(
        title="Access Token",
        description= "",
        required = True)

    gdprPermission = schema.Bool(
        title = """To register me, manage logins using cookies, and to send me email notifications(not news) as required.""",
        required = True,
        default = False)
    
    gdprPermission.text = """ <p> I give permission 
to process my professional information for the following  
purposes:</p>"""

    frequencyPermission = schema.Choice(
        vocabulary=SimpleVocabulary.fromValues(
                  ['Daily','Weekly','Monthly','Seldom','Never',''],
                  ),
        title = "To send me the news:",
        required = False,
        default = '',
    )  



