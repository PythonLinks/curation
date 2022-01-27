from zope.interface import Interface
from zope import schema
from z3c.schema.email  import RFC822MailAddress as Email
from zope.schema.vocabulary import SimpleVocabulary,SimpleTerm


class IApprove(Interface):
    webApproved = schema.Bool(
        title = "Approved for publication on the web.",
        required = False,
        default = False)

    emailApproved = schema.Bool(
        title = "Approved for publication in Emails.",
        required = False,
        default = False)

    private = schema.Bool(
        title = "Should this page be private?",
        required = False,
        default = False)    
    
    """
    hidden = schema.Bool(
        title = "Hidden from the public.Login Required.",
        description = "" "When this is checked, unauthorized viewers get a message "You are not permitted to view that page."  This discourages spammers.  For 
        publicly visible pages, this should be unchecked. "" ",
        required = False,
        default = False)
     """

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
    
    password = schema.Password(
        title="Password",
        description = "Be Strong",
        required = True)
    
class IPermissions(Interface):            

    chatPermission = schema.Bool(
        title = """To register me, manage logins using cookies, and to send me email notifications(not news) as required.""",
        required = True,
        default = False)

    newsPermission = schema.Bool(
        title = """To send me the news.""",
        required = False,
        default = False)    
    
    chatPermission.text = """ <p> I give permission 
to process my personal information for the following  
purposes:</p>"""

class IRegister(IHandle, IEmail, IPermissions):
   pass
