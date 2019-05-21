from zope import schema

from zope.interface import Interface

from dolmen.container import IBTreeContainer
from cromlech.container.interfaces import IOrdered

from zopache.pages.interfaces import ILocationBase
from zopache.pages.interfaces import IMap as IMapBase
from zopache.crud.interfaces import IContainer
from zopache.crud.interfaces import IContainer
from zopache.ttw.interfaces import IUntrustedHTML, IBranch, ICanonical
from zopache.pages.interfaces  import ICountable

class ICompany (ILocationBase,IContainer,IOrdered ,IBTreeContainer,IUntrustedHTML,ICanonical, ICountable):

    title = schema.TextLine(
        title = 'Company Name',
        description = u'What is this company called?',
        required = True,
    )

    url = schema.TextLine(
        title = u'The Company URL',
        description = 'Please link to the Company.',
        required = False,
    )

    jobURL = schema.TextLine(
        title = u'Jobs Page URL',
        description = 'Where do they list their jobs?',
        required = False,
    )        

    description= schema.Text(
        title = u'Specialization (20 characters)',
        description = " Why is this Company special?",
        required = False,
        max_length = 20,
        default = '',
    )
     
    source= schema.Text(
        title = u'Content',
        description = u'Please describe this company further.',
        required = False,
        default = '',
    )

    address= schema.Text(
        title = u'Company Address',
        description = """This is used to 
                 locate the company on the map.""",
        required = False,
        default = '',
    )    


class IMap (IMapBase):
    pass
