from zope import schema

from zope.interface import Interface

from dolmen.container import IBTreeContainer
from cromlech.container.interfaces import IOrdered

from zopache.pages.interfaces import ILocationOrMap
from zopache.crud.interfaces import IContainer
from zopache.ttw.interfaces import IUntrustedHTML, IBranch, ICanonical
from zopache.core.interfaces import ICountable
from zopache.pages.interfaces  import (
                                       ILocationContainer,
                                       ILocationLeaf)
from z3c.schema.email import RFC822MailAddress as Email

from zopache.pages.interfaces import IPage, ITime
from zopache.business.ifollow import IFollow

class IClass(Interface):
    json= schema.Text(
        title = 'Json Data',
        required = True,
        default = '{}',
    )
    
class IPolitician(IClass):
    pass


class ICity (ILocationContainer):
    address= schema.Text(
        title = u'City Address',
        description = """This is used to locate the city  on the map.  You only need the name of the city and country """,
        required = False
    )
    

class IRegion(ILocationContainer):
    pass

    
class IEventBase(IPage,IFollow,ITime):
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

    joinURL = schema.URI(
        title = u'The Meetup URL',
        description = """How to join this meetup.  Maybe include a link to the 
discord server invite.   Include  'https://'""",
        required = False,
        missing_value ='',
    )    
    
    source= schema.Text(
        title = 'More Informatton',
        description = 'Please provide more information about the event.',
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
        missing_value = "",
           
    )    

    time = schema.Datetime(title='Date and Time',
                           description = """ Use the format Day/Month/Year 
                   as in "12/30/19, 6:00 PM",
                whithout the quotation marks. 
     If you have diviculty with this widget, you can leave it blank, 
put the date and time in the "More Information" section and I will configure it later.
 In due course we will have a date time picker.""", 
                           required = False)

class IOnlineEvent(IEventBase):
    discordId= schema.TextLine(
        title = 'Your Discord Id',
        description = 'Can they contact you on Discord?',
        required = False,
    )
    
    joinURL = schema.URI(
        title = u'The Meetup URL',
        description = """How to join this meetup.  Maybe include a link to the 
discord server invite.   Include  'https://'""",
        required = False,
        missing_value ='',
    )    

       
from zopache.pages.interfaces import ITime
#ITime is on future events.
class IEvent(IEventBase,  ILocationLeaf):  
    address= schema.Text(
        title = u'Event Address',
           description = """Where is this event being held?""",
        required = True

    )        

from zopache.pages.interfaces import ILatLng


class ITreeBase (ILocationLeaf,IPage, IFollow):

    title = schema.TextLine(
        title = "Tree's Name",
        description = u'What will you call this tree?',
        required = True,
    )

    species= schema.Text(
        title = u'Species',
        description = " What type of tree is this?",
        required = True,
        max_length = 20,
     )
    
     
    description= schema.Text(
        title = u'Description (200 Characters)',
        description = "A short description of the tree. ",
        required = False,
        max_length = 200,
        default = '',
    )

    source= schema.Text(
        title = 'Content',
        description = 'Help people to love this tree.',
        required = False,
        default = '',
    )

    remoteURL = schema.URI(
        title = u'The Meetup URL',
        description = """How to join this meetup.  Maybe include a link to the 
discord server invite.   Include  'https://'""",
        required = False,
        missing_value ='',
    )    
    
class ITree(ITreeBase,ILatLng):
    pass
    

class ICompanyBase(ILocationContainer,IPage,IFollow):
    title = schema.TextLine(
        title = 'Company Name',
        description = u'What is this company called?',
        required = True,
    )

    remoteURL = schema.URI(
        title = u'The Company URL',
        description = """Please link to the Company. Include  'https://'""",
        required = False,
        missing_value ='',           
    )

    jobURL = schema.URI(
        title = u'Jobs Page URL',
        description = """Where are the jobs listed? 
                   Include  'https://' """,
        required = False,
        missing_value ='',           
    )

    specialization= schema.Text(
        title = u'Specialization ',
        description = " What is this Companies specialization? Make it really short",
        required = True,
        max_length = 200,
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
    address= schema.Text(
        title = u'Company Address',
        description = """This is used to 
                 locate the company on the map. List more than just the town, or else all the companies will just have one shared map pin. """,
        required = True

    )    

class IAddCompany(ICompany):    
    schema.Text(
        title = u'Company Address',
        description = """This is used to 
                 locate the company on the map. List more than just the town, or else all the companies will just have one shared map pin. """,
        required = True

    )    


    
    
class ISocialMedia(Interface):

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
    
    facebookId = schema.URI(
        title = u'FaceBook Page URL (Optional)',
        description = """Copy and paste the Facebook page URL. """,
        missing_value="",
        required = False,
    )

    facebookGroup = schema.URI(
        title = u'FaceBook Group (Optional)',
        description = """Copy and paste the Facebook GROUP URL. """,
        missing_value="",
        required = False,
    )

    youTubeChannelURL = schema.URI(
        title = u'YouTube Channel URL  (Optional)',
        description = """Copy and paste the YouTube Chanel  URL. """,
        missing_value="",
        required = False,
    )    

    email= Email(
        title = u'Email Address (Optional)',
        description = u'Can they email you? Make sure there are no spaces. ',
        required = False,
        missing_value = '',
    )
       
class IOnlineOrganization(
                ILocationContainer,IPage,
                          IFollow):
     pass          

class IOrganization(
                ILocationContainer,IPage,IFollow        
                    ):
     pass

from zopache.pages.interfaces import IMap as IMapBase
class IMap (IMapBase,IFollow):
    showCities = schema.Bool(
	    title = "Show Cities?",
	    description = "Should the table of companies show the city name?",           
	    required = False,
	    default = False)   

    showChildren = schema.Bool(
	    title = "Show Children?",
	    description = "Should it show the objects in the children?",           
	    required = False,
	    default = False)   
    
class IMapOrganizationBase(IOrganization):
    lattitude = schema.Float(
        title = u'Lattitude',
        description = u'Lattitude',
        min=-90.,
        max=90.,
        default = 51.509865,
        required = True,
        )

    longitude = schema.Float(
        title = u'Longitude',
        description = u'Longitude ',
        min=-180.,
        max=180.,
        default = 0.,
        required = True,
    )

    zoomLevel = schema.Float(
        title = u'Google Maps Zoom Level',
        description = u'Google Maps Zoom Level',
        min=0.,
        max=22.,
        default = 5., 
        required = True,
    )
    
    showChildren = schema.Bool(
	    title = "Show Children?",
	    description = "Should it show the objects in the children?",    
	    required = False,
	    default = True)
    
class IMapOrganization(IMapOrganizationBase,IMapBase):    
      pass

class IEndorsingOrganization(IMapOrganization,IMap):
       pass

class IMeetup (IPage,IFollow):
    title = schema.TextLine(
        title = 'Meetup Name',
        description = u'What is this meetup called?',
        required = True,
    )

    specialization= schema.Text(
        title = u'Specialization ',
        description = " What is this group's focus? Keep it really short.",
        required = True,
        max_length = 200,
        default = '',
    )
     
    description= schema.Text(
        title = u'Description (200 Characters)',
        description = "A short description of this meetup. ",
        required = False,
        max_length = 200,
        default = '',
    )

    source= schema.Text(
        title = u'Longer Description',
        description = u'Please describe this meetup further.',
        required = False,
        default = '',
    )    

    discordId= schema.TextLine(
        title = "Organizer's Discord Id",
        description = 'Can they contact you on Discord?',
        required = False,
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
        missing_value = ''
    )    

