from zope.interface import Interface
from zope import schema

class IRSSBase(Interface):
    pass

class IJustRSS(IRSSBase):
    rssURL=schema.URI(
        title = "Primary RSS URI",
        description ="""This is the source of new articles.  
              Please include "https://" or "http://".""",
        required = True,
        )
    
    htmlSummary=schema.Bool(
        title = "Is the Summary HTML?",
        description ="For those sources where the summary contains html tags",
        required = False,
        default = False,
        )


class IRSS(IRSSBase):
    title=schema.TextLine(
        title = "RSS Feed Name",
        description ="What is the web site called?",
        required = True,
        )

    description= schema.Text(
        title = 'Description',
        description = """A brief introduction of this RSS Source.  """,
        required = False,
        default = '',
    )    

    twitterId=schema.TextLine(
        title = "Twitter Id",
        description ="""Without the "@" sign?""",
        required = False,
        )
    
    remoteURL= schema.URI(
        title = 'URL',
        description = """A URL That this page refers to. 
             Please include 'https://'""",
        required = False,
    )
    
    rssURL=schema.URI(
        title = "Primary RSS URI",
        description ="""This is the source of new articles.  
              Please include "https://" or "http://".""",
        required = True,
        )

    logoURL=schema.URI(
        title = "Logo URL ",
        description ="An image is important",
        required = True,
        )
    

    htmlSummary=schema.Bool(
        title = "Is the Summary HTML?",
        description ="For those sources where the summary contains html tags",
        required = False,
        default = False,
        )        

    
class IRSSPage (IRSS):
      pass
