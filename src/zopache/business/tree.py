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


from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

items = [ ("decidous", "Decidous"),
          ("evergree", "Evergreen")]

terms = [ SimpleTerm(value=pair[0],
                     token=pair[0],
                     title=pair[1]) for pair in items ]

myVocabulary = SimpleVocabulary(terms)

class ITitle(Interface):
    title = schema.TextLine(
        title = "The Tree's Name",
        description = 'Please name the tree. Names cannot be changed later.',
        required = True,
    )

class ITreeBase (ILocationBase,IPage, IJoin):

    
    species = schema.Choice(
          title=u"Tree Species",
          vocabulary=myVocabulary,
          description = "What type of tree is this? This list will grow fast",
          )

    description= schema.Text(
        title = u'Description (200 Characters)',
        description = "A short description of this Tree.  Editable. ",
        required = False,
        max_length = 200,
        default = '',
    )
    
    source= schema.Text(
        title = 'Content',
        description = """Here you can say a lot more about the tree..""",
        required = False,
        default = '',
    )

class ITree(ITreeBase):
    pass


class IAddTree(ITitle,ITreeBase):    
    lattitude = schema.Float(
        title = u'Lattitude',
        description = 'How far from the equator is this tree.',
        min=-90.,
        max=90.,
        default = 51.509865,
        required = True,
        )

    longitude = schema.Float(
        title = u'Longitude',
        description = u'How far from London is this tee ',
        min=-180.,
        max=180.,
        default = 0.,
        required = True,
    )

from zopache.pages.location import LocationBase
from zopache.business.subscribe import Member

@implementer (ITree)
class Tree (LocationBase,Member):
    hidden = False
    longitude = 0.
    lattitude = 0.
    def __init__(self):
        LocationBase.__init__(self)
        Member.__init__(self)
    webClass = "Tree"
    clientClass = "category"


