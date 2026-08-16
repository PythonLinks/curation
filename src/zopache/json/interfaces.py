from zope.interface import Interface
from zope import schema

from cromlech.container.interfaces import IOrderedContainer

from zopache.pages.interfaces import IPageBase
from zopache.pages.interfaces import IPageBase, IContent
from zopache.crud.interfaces import ILeaf

class IJSONClass(IPageBase,IContent,IOrderedContainer):
    pass

class IMultilingual(IJSONClass):
    pass

class IMarkdown(IJSONClass):
    pass

class IJSONEvent(IMarkdown):
    pass

class IMultilingualLeaf(ILeaf):
    pass

class IClass(Interface):
    jsonData= schema.Text(
        title = 'Json Data',
        required = True,
        default = '{}',
    )

class IBasicJSON(IClass):
    pass

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
