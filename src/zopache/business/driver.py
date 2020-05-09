from zope import schema
from zope.interface import Interface
from zope.interface import implementer
from z3c.schema.email import RFC822MailAddress as Email

from cromlech.security import Unauthorized

from zopache.pages.page import Page
from zopache.business.company import GeoBase
from zopache.pages.interfaces import IPage, ILocationLeaf
from zopache.business.interfaces import IFollow, ILatLng, IAddress
from zopache.business.geocoding import Address
from zopache.pages.interfaces import IPage


class IDriverBase (ILocationLeaf,IPage):

    title = schema.TextLine(
        title = "Drivers's Legal Name",
        description = "What is the name on your driver's license?",
        required = True,
    )

    phone = schema.TextLine(
        title = "Drivers's Phone Number",
        description = "This is how riders will contact you",
        required = True,
    )

    email = Email(
        title="Your Email Address",
        description ="""This is how we will contact you. Your gmail address 
                      is best. """,
        required = True)
     
    description= schema.Text(
        title = u'Description (200 Characters)',
        description = "A short description of the ride you are offering.. ",
        required = False,
        max_length = 200,
        default = '',
    )

    pollingPlace = schema.TextLine(
        title = "The Name of the polling place.",
        description = """What is the name of the polling
                     place you will support.?""",
        required = True,
    )

    address= Address(
        title = "Polling Place Addess",
        description = """What is the address of the polling place 
                         you are supporting. """,
           required = True,
    )

    address= Address(
        title = "Polling Place Addess",
        description = """What is the address of the polling place 
                         you are supporting. This will be used to place
                         a pin on the map.""",
        required = True,
    )

    source= schema.Text(
        title = 'About Yourself',
        description = """Please say more about yourself.  It is good to 
                       link to your Facebook, Twitter and other 
                       social media accounts. And then 
                       link from your social 
                       media accounts to the page where you listed.  
                       That identifies you, gives the riders 
                       additional security, and reduces their risk. """,
        required = False,
        default = '',
    )
    
    GDPR = schema.Bool(
        title = "GDPR Permission",
        description = """ I hereby give permission for this web site to 
                          process my personal information for the purposes
                          of supporting a service of riding to the polls on 
                          primary and on election day.  And for the purpose
                          of providing me with notifications, 
                          logins, and cookie tracking""",
        required = True,
        )
                          


class IDriver(IDriverBase):
    pass

class IAddDriver(IDriverBase):    
    pass

@implementer (IDriver)
class Driver (GeoBase):
    webClass = "Driver"
    clientClass = "category"


