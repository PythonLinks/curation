from zope.interface import Interface
from zope import schema
from zopache.pages.interfaces import  ILinkBase
from z3c.schema.email  import RFC822MailAddress as Email
from zope.schema.vocabulary import SimpleVocabulary,SimpleTerm
from zopache.ttw.interfaces import IInternalPrincipal
from zopache.crud.interfaces import ILeaf, IContainer,IDeletable

from zopache.ttw.interfaces import IInternalPrincipal
class IAccount(IInternalPrincipal):
    pass

class IRemoteAccount(ILinkBase):    
    
    title=schema.TextLine(
        title = "Mastodon Account Name",
        description ="What is the account  called?",
        required = True,
        )
    
    description= schema.Text(
        title = 'Description',
        description = """The Mastodon Account BIo.  """,
        required = False,
        default = '',
    )    

    mastodonId=schema.TextLine(
        title = "Mastodon Id",
        description ="""@User@Domain""",
        required = False,
        )    

    defaultCategory = schema.TextLine(
        title = "Whereto place their recommended links",
        description ="This is the /slug where you can see their recommendedlinks.",
        required = False,
        )
    
    rssApproved=schema.Bool(
        title = "Is this feed approved for downloading",
        description ="We can block some feeds without deleting them.",
        required = False,
        default = True,
        )
    
    keepAllArticles=schema.Bool(
        title = "Keep all of their articles?",
        description ="Or clear out the old ones to save space?",
        required = False,
        default = True,
    )    
        
    domainName = schema.DottedName(
        title = 'Their Domain Name',
        description = 'Articles in this domain are listed, not approved.',
        required = False,
        missing_value = "",
    )
    
    wordsToAvoid = schema.Text(
        title = 'Words To Avoid',
        description = """These words will get the item rejected.  """,
        required = False,
        default = '',
    )
    

class IAddRemoteAccount(IRemoteAccount):
    logoURL=schema.URI(
        title = "Logo URL ",
        description ="An image is important",
        required = False,
        missing_value = '',
        )


class IToot(ILeaf,IDeletable):
    description= schema.Text(
        title = u'Description',
        description = """A brief introduction of this page.  
                        This is used by the search functions.""",
        required = False,
        default = u'',
    )

    source= schema.Text(
        title = 'Content',
        description = 'This is the main content for this page',
        required = False,
        default = '',
    )

  
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



