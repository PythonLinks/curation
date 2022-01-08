from zope.interface import Interface
from zope import schema
from zopache.crud.interfaces import IContainer , IZodbRoot
from dolmen.container import IBTreeContainer
from cromlech.container.interfaces import IOrderedContainer
from cromlech.browser.interfaces import IPublicationRoot


from zopache.ttw.interfaces import ISourceLeaf
from zopache.ttw.interfaces import IUntrustedHTML, IBranch, ICanonical
from zopache.python.interfaces import IDirectory
from zopache.ttw.interfaces import ISourceLeaf
from cromlech.file import FileField
from zopache.ttw.interfaces import IAceHTML
from zopache.core.interfaces import ICountable, ISiteRoot
from zopache.crud.interfaces import ILeaf
from zopache.ttw.interfaces import IJSON

class ILayoutView(Interface):
    pass

class IImaginary(ILayoutView):
   pass

class IImaginaryBTree(ILayoutView):
   pass

# A MARKER TO SHOW THAT THIS IS NEWS
class IRecent(Interface):
    pass

#THINGS THAT HAPPEN AT  A POINT IN TIME  
class ITime(Interface):
    pass

class IContent(ICanonical):
    pass

class IJSONInclude(Interface):
    pass

class IPageTop(Interface):
    
    title = schema.TextLine(
        title = u'Page Name',
        description = u'Describe this page.',
        required = True,
    )

class ILinkTop(Interface):
    title = schema.TextLine(
        title = 'Remote Page Name',
        description = 'What is the title of this link?',
        required = True,
    )
    
    remoteURL= schema.URI(
        title = 'URL',
        description = """A URL That this page refers to. 
             Please include 'https://'""",
        required = False,
    )
    
class IAddLinkTop(ILinkTop):    
    imageURL= schema.URI(
        title = 'Image URL',
        description = """A URL That this highlights this link. 
             Please include 'https://
             The image will be automatically downloaded'""",
        missing_value = '',
        required = False,
    )
    
class IPageBottom(Interface):

    description= schema.Text(
        title = 'Description',
        description = """A brief introduction of this page.  
                        This is used by the search functions.""",
        required = False,
        default = u'',
    )

    
    source= schema.Text(
        title = u'Content',
        description = u'This is the main content for this page',
        required = False,
        default = u'',
    )
    

class IActionNetwork(ILinkTop,
                     ILeaf,
                     IJSONInclude,
                     IOrderedContainer,
                     ICountable):
    description= schema.Text(
        title = 'Description',
        description = "A brief introduction to this Action.",
        required = True,
        default = u'',
    )       

class IPageBase(ICanonical):
    pass

class IPage(ILayoutView,IPageTop,IPageBottom,IPageBase,
            IContent, IOrderedContainer,
            IJSONInclude, IUntrustedHTML,IAceHTML):
    pass

class IMultilingual(IPageBase,ILayoutView,IContent,IOrderedContainer):
    pass

class IProxyPage(IPage):
    pass

class IAddPage(IPage):
    imagegURL= schema.URI(
        title = 'Image URL',
        description = """A URL That this page refers to. 
             Please include 'https://
             The image will be automatically downloaded'""",
        required = False,
    )        
      
class ILink(IPage,ILinkTop,ICountable):
    pass

class IAddLink(IPage, IAddLinkTop):
     pass
    
class IMarkdown (IAceHTML,ISourceLeaf):
    pass

from zopache.ttw.interfaces import IJSON
class INotebookBase(Interface):
    title = schema.TextLine(
        title = u'Notebook Title',
        description = u'What is the name of this notebook?.',
        required = True,
    )
    
    description= schema.Text(
        title = u'Description',
        description = """A brief introduction of this Notebook.  
                        This is used by the search functions.""",
        required = False,
        default = u'',
    )
    
from zopache.ttw.interfaces import IJSON
class INoteboko(INotebookBase,IJSON):
    source= schema.Text(
        title = u'Notebook Source:',
        description = u'This is the JSON  which defines the Notebook.',
        required = False,
        default = u'',
    )
    
class IAddNotebook(INotebookBase):    
    _v_source = FileField(
                    title=u'Upload a .pynib file',
                    required = True,
                      )    


class INotebook (ISourceLeaf,IDirectory):
    description= schema.Text(
        title = u'Description',
        description = """A brief introduction of this Notebook.  
                        This is used by the search functions.""",
        required = False,
        default = u'',
    )

class INews (IPage,IRecent):
    pass

#USED BY Green Maps
class IRootPage(ISiteRoot,
                IZodbRoot,
                IPage,
                IBranch):
    pass

class ISiteRootPage(ISiteRoot,IBranch,IPageBase,IBTreeContainer):
    pass



class INotPage (Interface):
     pass

class IGeography(Interface):    
    pass

class ILatLng(Interface):
    lattitude = schema.Float(
        title = u'Lattitude',
        description = u'Lattitude',
        min=-90.,
        max=90.,
        default = 51.509865,
        required = True,
        )

    longitude = schema.Float(
        title = u'Longitude',
        description = u'Longitude ',
        min=-180.,
        max=180.,
        default = 0.,
        required = True,
    )

#This is the legacy Location,
#Used in pages.location.Location
#So it has to stay
class ILocation(IGeography,ILatLng):
    pass

#For Politicians
class ILocationLeaf(ILocation):
    pass

#For State Party Organizations
class ILocationContainer(ILocation):
    pass

class IPin(ILocationLeaf,ILatLng,IGeography):
    pass

class IMap(IGeography,ILatLng):
    zoomLevel = schema.Float(
        title = u'Google Maps Zoom Level',
        description = u'Google Maps Zoom Level',
        min=0.,
        max=22.,
        default = 5., 
        required = True,
    )

class ISimpleMap(IPage,IMap):
    pass
    
from zopache.pages.address import Address
class IAddress(Interface):
    pass
    """"
    address= Address(
        title = u'Address (For the map)',
        description = u'Where is the main office for this company?',
        required = True,
        default = u'',
    )
    """
    
class IAddressMap(IMap,IAddress):
    pass

class ICategory(IJSON,IPageBase):
    title = schema.TextLine(
        title = 'Category Name',
        description = 'Name this category..',
        required = True,
    )

    twitterIds = schema.TextLine(
        title = 'Twitter Ids',
        description = "Accounts to Notify",
        required = False,
        default = '',
    )
    
    description= schema.Text(
        title = 'Description',
        description = "A brief description of this category",
        required = False,
        default = '',
    )
    

    tags = schema.TextLine(
        title = 'Tags',
        description = 'For this Cateogry.',
        required = False,
    )

class IGeographicalCategory(ICategory, IGeography):
    title = schema.TextLine(
        title = 'Geographical Category Name',
        description = u'Describe this page.',
        required = True,
    )

    description= schema.Text(
        title = 'Description',
        description = """A brief introduction of this geographical category..  
                        This is used by the search functions.""",
        required = False,
        default = '',
    )

class ILocationCategory (IGeographicalCategory, ILatLng):
    pass

class IRegionCategory(IGeographicalCategory):
    pass

class IMapCategory(IGeographicalCategory,ILatLng):
    pass
