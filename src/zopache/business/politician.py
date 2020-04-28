from zope import schema
from zope.interface import Interface
from zope.interface import implementer
from z3c.schema.email import RFC822MailAddress as Email

from cromlech.security import Unauthorized

from zopache.pages.interfaces import ILocationLeaf, IPage
from zopache.pages.page import Page
from zopache.business.company import GeoBase
from zopache.business.interfaces import IJoin, ILatLng, IAddress, ISocialMedia
from zopache.business.geocoding import Address
from zopache.pages.interfaces import IPage

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm



items = [ ("sunshineMovement", "Sunshine Movemement"),
          ("courageToChange","Courage To Change"),
          ("justiceDemocrats","Justice Democrats")
          ]

terms = []
for item in items:
    new = SimpleTerm(value=item[0],
                     token=item [0],
                     title=item[1] )
    terms.append(new)

myVocabulary = SimpleVocabulary(terms)

def getVocabulary(context):
    return myVocabulary

from zopache.ttw.editprincipal import possibleItems
class IPoliticianBase (ILocationLeaf):

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
        title = "The Politician's Website",
        description = """Please link to the Politician. Include  'https://'""",
        required = False,
    )
    imageURL = schema.URI(
        title = "The Politician's Image",
        description = """Please link to the Politician. Include  'https://'""",
        required = False,
    )
    districtURL = schema.URI(
        title = "The Politician's District Map",
        description = """Please link to the Politician. Include  'https://'""",
        required = False,
    )    
    
#    endorsedBy = schema.Collection(
#          value_type = schema.Choice( vocabulary = myVocabulary),        
#          title=u"Endorsed By",
#          description = "Which organizations endorsed this politician?",       
#          )
#    endorsedBy.mode = 'multiselect'
    
    source= schema.Text(
        title = 'Content',
        description = """Please describe this politician further. Add relevant links, and links to images.""",
        required = False,
        default = '',
    )


    phone= schema.TextLine(
        title = u'Phone Number (Optional)',
        description = u'Can they call you?',
        required = False,
        default = '',
    )

    twitterId= schema.TextLine(
        title = u'TwitterId (Optional)',
        description = u'Do not include the @ symbol.',
        required = False,
        default = '',
    )    

    facebookId= schema.TextLine(
        title = u'FaceBook Id (Optional)',
        description = u'Not the domain name, just the part after "https/facebook.com/". ',
        required = False,
        default = '',
    )

    facebookGroup= schema.TextLine(
        title = u'Facebook Group (Optional)',
        description = 'Not the domain name, Just the part after https://facebook.com/groups/',
        required = False,
        default = '',
    )

    instagramId= schema.TextLine(
        title = u'Instagram Id (Optional)',
        description = 'Not the domain name, Just the part after https://facebook.com/groups/',
        required = False,
        default = '',
    )        

    email= Email(
        title = u'Email Address (Optional)',
        description = u'Can they email you? Make sure there are no spaces. ',
        missing_value = "",
        required = False,
    )
    
    address= Address(
        title = "Politician's District Office Address",
        description = """This is used to 
                 locate the politician on the map. """,
           required = True,
    )

class IPolitician(IPoliticianBase,ISocialMedia):
    pass

@implementer (IPolitician)
class Politician (GeoBase):
    webClass = "Politician"
    clientClass = "category"


