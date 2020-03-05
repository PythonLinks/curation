from zope import schema
from zope.interface import Interface
from zope.interface import implementer
from z3c.schema.email import RFC822MailAddress as EmailBase

from cromlech.security import Unauthorized

from zopache.pages.interfaces import ILocationBase
from zopache.pages.page import Page
from zopache.business.company import Base
from zopache.pages.interfaces import IPage, ILocationBase
from zopache.business.interfaces import IJoin, ILatLng, IAddress
from zopache.business.geocoding import Address
from zopache.pages.interfaces import IPage

class IPoliticianBase (ILocationBase,IPage, IJoin):

    title = schema.TextLine(
        title = "Politician's Name",
        description = u'Who is this politician?',
        required = True,
    )
     
    description= schema.Text(
        title = u'Description (200 Characters)',
        description = "A short description of the politician. ",
        required = False,
        max_length = 200,
        default = '',
    )
    url = schema.URI(
        title = "The Politician's URL",
        description = """Please link to the Politician. Include  'https://'""",
        required = False,
    )
    source= schema.Text(
        title = 'Content',
        description = """Please describe this politician further. Add relevant links, and links to images.""",
        required = False,
        default = '',
    )
    address= Address(
        title = "Politician's Home Office Address",
        description = """This is used to 
                 locate the politician on the map. """,
           required = True,
    )

class IPolitician(IPoliticianBase,IAddress):
    pass


class IAddPolitician(IPoliticianBase, IAddress):    
    pass


@implementer (IPolitician)
class Politician (Base):
    webClass = "Politician"
    clientClass = "category"


