from zope.interface import Interface
from zope import schema
from zopache.pages.interfaces import  ILinkBase
from z3c.schema.email  import RFC822MailAddress as Email
from zope.schema.vocabulary import SimpleVocabulary,SimpleTerm

from zopache.crud.interfaces import IContainer
from zopache.pages.interfaces import IPageBase
from zopache.pages.interfaces import ILinkBase

class IMastodonArticles(IPageBase):    
    
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

    keepAllArticles=schema.Bool(
        title = "Keep all of their articles?",
        description ="Or clear out the old ones to save space?",
        required = False,
        default = True,
        )    


class IArticle(ILinkBase):

    title = schema.TextLine(
        title = 'Remote Article Name',
        description = 'What is the title of this link?',
        required = True,
    )

    remoteURL= schema.URI(
        title = 'Article URL',
        description = 'The url of the remote article',
        required = False,
    )
    
    description= schema.Text(
        title = u'Description',
        description = """A brief introduction of this page.  
                        This is used by the search functions.""",
        required = False,
        default = u'',
    )

    source= schema.Text(
        title = 'Content',
        description = 'This is the main content for this article',
        required = False,
        default = '',
    )

  
