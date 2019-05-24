from zope.interface import Interface
from zope import schema
from zopache.crud.interfaces import IContainer
from dolmen.container import IBTreeContainer
from cromlech.container.interfaces import IOrdered
from cromlech.browser.interfaces import IPublicationRoot
from zopache.ttw.interfaces import IUntrustedHTML, IBranch, ICanonical

# A MARKER TO SHOW THAT THIS IS NEWS
class IRecent(Interface):
    pass

class ICountable(Interface):
      pass

class IPage(IContainer,IOrdered ,IBTreeContainer,IUntrustedHTML,ICanonical):

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
        required = False,
        default = u'',
    )
     
    source= schema.Text(
        title = u'Content',
        description = u'This is the main content for this page',
        required = False,
        default = u'',
    )

class INews (IPage,IRecent):
    pass

class IRootPage(IBranch,IPublicationRoot,IPage):
    pass

class INotPage (Interface):
     pass


    

class ILocationBase(IPage):    
    pass

class ILocationBase2(ILocationBase):    
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
    
class ILocation(ILocationBase2, IRecent):
    pass

class IMap(ILocationBase2):
    zoomLevel = schema.Float(
        title = u'Google Maps Zoom Level',
        description = u'Google Maps Zoom Level',
        min=0.,
        max=22.,
        default = 5., 
        required = True,
    )
    """
from .geo import Address

    mapWidth = schema.Float(
        title = u'Map Width',
        description = u'Map Width ',
        min=-0.,
        max=20000.,
        required = True,
    )
    
    mapHeight = schema.Float(
        title = u'mapHeight',
        description = u'mapHeight ',
        min=0.,
        max=20000.,
        required = True,
    )    

    address= Address(
        title = u'Address (For the map)',
        description = u'Where is the main office for this company?',
        required = True,
        default = u'',
    )
    """
 
