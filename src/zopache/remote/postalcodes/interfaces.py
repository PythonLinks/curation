from zope import schema
from zope.interface import Interface, invariant, Invalid
from zopache.pages.interfaces import (ILocation,
                                      IPage,
                                      IPageBase)

from zopache.json.interfaces import IClass

class IGDPRForm(Interface):
        
    countryName  = schema.TextLine(
        title='Your country', required=False)

    postalCode  = schema.TextLine(
        title='Your Postal code', required=False,
        default = "")

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

    city  = schema.TextLine(
        title='Your city', required=False,
        default = "")

    region  = schema.TextLine(
        title='Your state or province', required=False,
        default = "")        

    @invariant
    def checkForBothCountryAndCountryPostalCodeOrNeither(data):
        if bool(data.countryCode) != bool(data.postalCode):
            if (data.countryCode):
                message = ("You entered a country name, the country code "
                           "was correctly calculated, but there "
                           "was no postal code provided. Please enter a "
                           "postal code or delete the country name. "
                           "Not providing both country and postal code will "
                           "hide the link to your fediverse account.")
            else:
                message = ("You entered a postal code, but the mapbox api "
                          "was not able to calculate the country code.")
            raise Invalid(message)

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
    gdprPermission.text = """
    <p> Please enter both Country Name and Postal Code.  To not be listed enter neither one. </p>
    <p> I give permission 
to process my personal information for the following  
purposes:</p>"""

class ICountryPostalCode(ILocation, IPage):
    pass

    
