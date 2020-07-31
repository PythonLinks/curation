from zope import schema
from zope.interface import Interface
from zope.interface import implementer
from z3c.schema.email import RFC822MailAddress as Email

from cromlech.security import Unauthorized

from zopache.pages.interfaces import ILocationLeaf, IPage
from zopache.pages.page import Page,RootPage
from zopache.business.company import GeoBase
from zopache.business.interfaces import IFollow, ILatLng, IAddress, ISocialMedia
from zopache.business.geocoding import Address
from zopache.pages.interfaces import IPage,IRootPage

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zopache.application.choices import fromList
from zopache.ttw.treewidget import TreeField
from zopache.pages.location import LocationLeaf

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
class IPoliticianBase (ILocationLeaf,IFollow):

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

    status = schema.Set(
        value_type = schema.Choice(source = fromList(['Elected',
                                                      'Running',
                                                      'Former'])),
        title="Already Elected Or Running For Office",
        description= "It could be both",
        required = False,)

    localOrNational = schema.Set(
        value_type = schema.Choice(source = fromList(['Local','State-Wide','National'])),
        title="Local Or National",
        description= "Are they running for local or congressional office",
        required = False,)    
    
#    addTo=TreeField(
#           title="Where to Add this Politician.",
#           description= "State-wide politicians get added to the state party, #Local Politicians get added to the local party if there is one.  ?",
#           required = True,
#            )
    
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
    )

    remoteURL = schema.URI(
        title = "The Politician's Website",
        description = """Please link to the Politician. Include  'https://'""",
        missing_value="",
        required = False,
    )
    

    districtURL = schema.URI(
        title = "The Politician's District Map",
        description = """Please link to the Politician. Include  'https://'""",
        required = False,
        missing_value="",                
    )    

    phone= schema.TextLine(
        title = u'Phone Number (Optional)',
        description = u'Can they call you?',
        required = False,
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
        description = u'Can they email you? Make sure there are no spaces.. ',
        missing_value = "",
        required = False,
    )
    
    address= Address(
        title = "Politician's District Office Address",
        description = """This is used to 
                 locate the politician on the map. """,
           required = True,
    )

class IPolitician(IPoliticianBase):
    pass


from zopache.pages.interfaces import ISiteRoot
class IPoliticiansSite(IPolitician,ISiteRoot):
   pass

class IAddPolitician(IPolitician):
    imageURL = schema.URI(
        title = "The Politician's Image",
        description = """Please link to the Politician. Include  'https://'""",
        missing_value="",        
        required = False,
    )   
    
@implementer (IPolitician)
class Politician (GeoBase,LocationLeaf):
    webClass = "Politician"
    clientClass = "category"

from zopache.pages.page import SiteRoot    
@implementer (IPoliticiansSite)
class PoliticiansSite (GeoBase,LocationLeaf,SiteRoot):
    webClass = "Politician"
    clientClass = "category"    
    def __init__(self):
        SiteRoot.__init__(self)
        GeoBase.__init__(self)
        LocationLeaf.__init__(self)
