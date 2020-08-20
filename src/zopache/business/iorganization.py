from zope import schema
from zope.schema.vocabulary import SimpleVocabulary
from zope.interface import Interface
from zope.interface import directlyProvides
from zope.schema.interfaces import IContextSourceBinder

from zopache.application.choices import fromDict
from zopache.ttw.acquisition import ParentalAcquire
from zopache.ttw.treewidget import TreeField
from zopache.application.choices import fromList

def possibleFocus (context):
    return fromDict(getDict(context))

def getDict(context):        
    choices = ParentalAcquire(context)['focusChoices']
    if ((choices != None) and
        (choices.__class__.__name__ == 'PythonScript')):
        return choices()
    return {}    

directlyProvides(possibleFocus, IContextSourceBinder)

class IOrganizationBase (Interface):
    title = schema.TextLine(
        title = 'Organization Name',
        description = u'What is this organization called?',
        required = True,
    )

    description= schema.Text(
        title = u'Description (200 Characters)',
        description = "A short description of this organization. ",
        required = False,
        max_length = 200,
        default = '',
    )

    focus = schema.Choice(
        source = possibleFocus,
        title="Specialization",
        description= "What is this groups focus?",
        required = False)
    
    ballotStatus = schema.Choice(
        source = fromList(['On Ballot',
                           'Petitioning',
                           'Minor Party',
                           'Independent',
                           'Write-In',
                           'Unrecognized']),
        title="Ballot Status?",

        description= "One of four.",
        default = "On-Ballot",
        required = False,)
#    addTo=TreeField(
#           title="Where should this organization be?",
#           description= "To be approved, please place it in a leaf of the tree.?",
#           required = True,
#           )    
    #was url
    remoteURL = schema.URI(
        title = u'The Organization URL',
        description = """Please link to a web page, maybe twitter or gab.com 
. Include  'https://'""",
        required = False,
        missing_value ='',           
    )

    source= schema.Text(
        title = u'Longer Description',
        description = u'Please describe this organization further.',
        required = False,
        default = '',
    )    
