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

class ISubscribe(IEmail, IPermissions):
    pass
