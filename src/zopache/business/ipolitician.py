from zope import schema
from zope.interface import Interface
from z3c.schema.email import RFC822MailAddress as Email
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zopache.pages.address import Address
from zopache.pages.interfaces import IPage,IRootPage,ILocationLeaf
from zopache.application.choices import fromList
from zopache.ttw.treewidget import TreeField
from zopache.business.ifollow import IFollow
from zopache.business.interfaces import (
                                         ILatLng,
                                         IAddress,
                                         IOrganizationOrPolitician,
                                         ISocialMedia)

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
class IPoliticianBase (ILocationLeaf,IFollow,IOrganizationOrPolitician):

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
        value_type = schema.Choice(source = fromList(['Local','State','National'])),
        title="Local Or National",
        description= "Are they running for local or congressional office",
        required = False,)    

    affiliation = schema.Choice(
        source = fromList(['Green Party',
                           'Independent',
                           'Write In']),
        title="Ballot Status",
        description= "One of three.",
        default = "Green-Party",
        required = True,)

    
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
    
    remoteURL = schema.URI(
        title = "The Politician's Website",
        description = """Please link to the Politician. Include  'https://'""",
        missing_value="",
        required = False,
    )

    source= schema.Text(
        title = 'Content',
        description = """Please describe this politician further. Add relevant links, and links to images.""",
        required = False,
    )

    eventsPageURL = schema.URI(
        title = "Events Page URL ",
        description = """An optional link to their events page.  Please include   'https://'""",
        missing_value="",
        required = False,
    )
    
    hasScheduledEvents = schema.Bool(
	    title = "Does the events page have events scheduled?",
	    description = """If so, then the pin will light up. """,
	    required = False,
	    default = False)    
    
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

    facebookId = schema.URI(
        title = u'FaceBook URL  (Optional, Not the Group URL.)',
        description = """Copy and paste the Facebook URL (Not the Group). """,
        missing_value="",
        required = False,
    )

    facebookGroup = schema.URI(
        title = u'FaceBook Group URL (Optional)',
        description = """Copy and paste the Facebook GROUP url. """,
        missing_value="",
        required = False,
    )    
    

    instagramId= schema.TextLine(
        title = u'Instagram Id (Optional)',
        description = 'Not the domain name, Just the part after https://instagram.com/',
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
