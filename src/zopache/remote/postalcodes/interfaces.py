from zope import schema
from zope.interface import Interface
from zopache.pages.interfaces import (ILocation,
                                      IPage,
                                      IPageBase)

from zopache.json.interfaces import IClass

class IGDPRForm(Interface):
        
    countryName  = schema.TextLine(
        title='Your country', required=False)

    postalCode  = schema.TextLine(
        title='Your PostalCode', required=False,
        default = "",
        description = "Please enter both Country Name and Postal Code.  To not be listed enter neither one. ")    

    gdprPermission = schema.Bool(
        title = """To run this web site, including cookie-based logins.""",
        required = True,
        default = False)

    linkPermission = schema.Bool(
        title = ("To add a link to my Mastodon or Fediverse account from " +
                "the page for my postal code."),
        required = False,
        default = False)

    countryCode  = schema.TextLine(
        title='Your country code', required=False,
        default = "")    

    latitude = schema.Float(
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
    gdprPermission.text = """ <p> I give permission 
to process my personal information for the following  
purposes:</p>"""

class IPostalCountryCode(ILocation, IPage):
    pass
    
class IPerson (IPageBase):
    pass    
