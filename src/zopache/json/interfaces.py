from zope.interface import Interface
from zope import schema
from zopache.pages.interfaces import IPageBase

class IClass(Interface):
    json= schema.Text(
        title = 'Json Data',
        required = True,
        default = '{}',
    )
    
class INewsLetter(IClass):
    pass

class IAddNewsLetter(IPageBase):
    title = schema.TextLine(
        title = 'Newsletter Name',
        description = 'Name this newsletter.',
        required = True,
    )
    
    originalURL= schema.URI(
        title = 'URL',
        description = "The Substack article",
        required = False,
    )    
