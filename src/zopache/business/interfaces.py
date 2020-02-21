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
from zopache.ttw.interfaces import IUserHTML
from z3c.schema.email import RFC822MailAddress as EmailBase
from zopache.business.geocoding import Address
from zopache.pages.interfaces import IPage

class Email(EmailBase):
    def _validate (self,data):
       if data == "":
          return
       EmailBase._validate(self,data)


class IAddress(Interface):
       pass

class IJoin(Interface):
    pass

class IEvent(IAddress, IPage,ILocationBase, IJoin):  
    title = schema.TextLine(
        title = 'Event Name',
        description = u'What is this event called?',
        required = True,
    )

    description= schema.Text(
        title = u'Description (200 Characters)',
        description = "A short description of the event. ",
        required = False,
        max_length = 200,
        default = '',
    )

    phone= schema.TextLine(
        title = u'Phone Number (Optional)',
        description = u'Can they call you?',
        required = False,
        default = '',
    )

    email= Email(
        title = u'Email Address (Optional)',
        description = u'Can they email you? Make sure there are no spaces. ',
        required = False,
    )    

    source= schema.Text(
        title = u'More Informatton',
        description = u'Please more information about the event.',
        required = False,
        default = '',
    )

    time = schema.Datetime(title='Date and Time',
                           description = """ Use the format Day/Month/Year 
                   as in "12/30/19, 6:00 PM",
                whithout the quotation marks. In due course 
                           we will have a date time picker.""", 

                           required = True)
    
    address= Address(
        title = u'Event Address',
        description = """This is used to 
                 locate the event on the map. """,
           required = True,
    )

class ICompanyOrOrganization (IAddress, ILocationBase,
                              IPage, IJoin):
    pass

class ICompanyBase(ICompanyOrOrganization):
    title = schema.TextLine(
        title = 'Company Name',
        description = u'What is this company called?',
        required = True,
    )

    url = schema.URI(
        title = u'The Company URL',
        description = """Please link to the Company. Include  'https://'""",
        required = False,
    )

    jobURL = schema.URI(
        title = u'Jobs Page URL',
        description = """Where are the jobs listed? 
                   Include  'https://' """,
        required = False,
    )

    specialization= schema.Text(
        title = u'Specialization (20 characters)',
        description = " Why is this Company special?",
        required = True,
        max_length = 20,
        default = '',
    )
     
    description= schema.Text(
        title = u'Description (200 Characters)',
        description = "A short description of the company. ",
        required = False,
        max_length = 200,
        default = '',
    )

    source= schema.Text(
        title = u'Content',
        description = u'Please describe this company further.',
        required = False,
        default = '',
    )

class ICompany(ICompanyBase):    
    address= Address(
        title = u'Company Address',
        description = """This is used to 
                 locate the company on the map. List more than just the town, or else all the companies will just have one shared map pin. """,
        required = True

    )    

class IAddCompany(ICompany):    
    address= schema.Text(
        title = u'Company Address',
        description = """This is used to 
                 locate the company on the map. List more than just the town, or else all the companies will just have one shared map pin. """,
        required = True

    )    
    
class IOrganizationBase (ICompanyOrOrganization):
    title = schema.TextLine(
        title = 'Organization Name',
        description = u'What is this organization called?',
        required = True,
    )

    url = schema.URI(
        title = u'The Organization URL',
        description = """Please link to a web page, maybe twitter or gab.com 
. Include  'https://'""",
        required = False,
    )

    specialization= schema.Text(
        title = u'Specialization (20 characters)',
        description = " Why is this groups focus?",
        required = True,
        max_length = 20,
        default = '',
    )
     
    description= schema.Text(
        title = u'Description (200 Characters)',
        description = "A short description of this organization. ",
        required = False,
        max_length = 200,
        default = '',
    )

    source= schema.Text(
        title = u'Longer Description',
        description = u'Please describe this organization further.',
        required = False,
        default = '',
    )    

    phone= schema.TextLine(
        title = u'Phone Number (Optional)',
        description = u'Can they call you?',
        required = False,
        default = '',
    )

    email= Email(
        title = u'Email Address (Optional)',
        description = u'Can they email you? Make sure there are no spaces. ',
        required = False,
    )    

class IOrganization(IOrganizationBase):    
    address= Address(
        title = u'Organization Address',
        description = """This is used to 
                 locate the organization on the map.  You need at least a street name.  If you only give the city, multiple organizations will share the same pin, and only one will be visible. """,
        required = False
    )

class IAddOrganization(IOrganizationBase):    
    address= schema.Text(
        title = u'Organization Address',
        description = """This is used to 
                 locate the organization on the map.  You need at least a street name.  If you only give the city, multiple organizations will share the same pin, and only one will be visible. """,
        required = False
    )        
    


class IMap (IMapBase):
    showCities = schema.Bool(
	    title = "Show Cities?",
	    description = "Should the table of companies show the city name?",           
	    required = False,
	    default = False)   

