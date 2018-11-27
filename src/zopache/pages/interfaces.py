from zope.interface import Interface
from zope import schema
from zopache.crud.interfaces import IContainer
from dolmen.container import IBTreeContainer
from cromlech.container.interfaces import IOrdered
from cromlech.browser.interfaces import IPublicationRoot

from zopache.ttw.interfaces import IUntrustedHTML

class IPage(IContainer,IOrdered ,IUntrustedHTML):

    title = schema.TextLine(
        title = u'Page Name',
        description = u'Describe this page.',
        required = True,
    )

#    url = schema.URI(
#        title = u'URL (Optional)',
#        description = u'A URL That this page refers to.',
#        required = False,
#    )    

    description= schema.Text(
        title = u'Description',
        description = """A brief introduction of this page.  
                        This is used by the search functions.""",
        required = True,
        default = u'',
    )
     
    source= schema.Text(
        title = u'Content',
        description = u'This is the main content for this page',
        required = False,
        default = u'',
    )

    
class IRootPage(IPublicationRoot,IPage):
    pass

class INotPage (Interface):
     pass
