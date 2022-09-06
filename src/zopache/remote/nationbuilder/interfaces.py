from zope.interface import Interface
from zope import schema

class IFetchData (Interface):
    imageURL= schema.URI(
        title = 'Image URL',
        description = 'The url of the remote image.  Please include "https://"',
        required = False,
    )      

    remoteURL= schema.URI(
        title = 'URL',
        description = 'The url of the remote web page.  Please include "https://"',
        required = True,
    )      

    
