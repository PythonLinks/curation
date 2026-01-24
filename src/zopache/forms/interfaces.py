from zope.interface import Interface
from zope import schema
from z3c.schema.email  import RFC822MailAddress as Email
from zope.schema.vocabulary import SimpleVocabulary,SimpleTerm


class IApprove(Interface):
    webApproved = schema.Bool(
        title = "Approved for publication on the web.",
        required = False,
        default = False)

class ILogin(Interface):

    email  = schema.TextLine(
        title='Username or Email Address', required=True)

    password = schema.Password(
        title='Password', required=True)


class IHandle(Interface):

    handle = schema.DottedName(
        title="User Name (handle)",
        description= "Legal characters are (a-Z), (0-9), '.' and '_'. Spaces are not allowed.",
        required = True)

class IEmail(Interface):    
    email = Email(
        title="Your Email Address",
        description ="",
        required = True)
    
class IPassword(Interface):    
    password = schema.Password(
        title="Password",
        description = "Be Strong",
        required = True)
    
class IGDPRForm(Interface):
    yourName = schema.TextLine(
        title="Your name",
        default = '' ,
        required = True)

    mastodonId = schema.TextLine(
        title="Mastodon or Discord Id (@me@discord.com)",
        default = '' ,
        required = False)

    emailAddress = schema.TextLine(
        title="Or your Email Address",
        required = False)
        
    gdprPermission = schema.Bool(
        title = """To manage events and run this web site, including cookie-based logins.""",
        required = True,
        default = False)

    newsPermission = schema.Bool(
        title = "To send me ASIC and FPGA technology news.",
        required = False,
        default = False)
    
#    postalPermission = schema.Bool(
#        title = """To add a link to my Mastodon or Fediverse account from the page for my zip code.""",
#        required = False,
#        default = False)

#    postalCode  = schema.TextLine(
#        title='Your US Zip Code', required=False,
#        default = "")    

    gdprPermission.text = """ <p> I give permission 
to process my personal information for the following  
purposes:</p>"""


