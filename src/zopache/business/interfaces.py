from zope.interface import Interface
from zopache.pages.interfaces import ILocation
from zopache.pages.interfaces import ILocation as IMapBase

class ICompany (ILocationBase,IContainer,IOrdered ,IBTreeContainer,IUntrustedHTML,ICanonical):

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
        max_len = 20,
        default = '',
    )
     
    source= schema.Text(
        title = u'Content',
        description = u'Please describe this company further.',
        required = False,
        default = '',
    )

    address= schema.Text(
        title = u'Their Office Address',
        description = """Once the posting is approved, this is Used to 
                 locate the company on the map.""",
        required = False,
        default = '',
    )    


class IMap (IMapBase):
    pass
