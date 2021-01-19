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
    pass
    
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
