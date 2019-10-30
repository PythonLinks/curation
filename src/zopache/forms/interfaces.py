from zope.interface import Interface
from zope import schema
from z3c.schema.email  import RFC822MailAddress as Email
from zope.schema.vocabulary import SimpleVocabulary,SimpleTerm

class ILogin(Interface):

    email  = schema.TextLine(
        title='Username or Email Address', required=True)

    password = schema.Password(
        title='Password', required=True)


class IGLogin(Interface):
        idtoken= schema.Text(
        title="Token",
        description= "",
        required = True)
        

class IHandle(Interface):

    handle = schema.DottedName(
        title="User Name",
        description= "Legal characters are (a-Z), (0-9), '.' and '_'.",
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
        title = "Run this web server.",
        required = True,
        default = False)
    chatPermission.text = """ <p> I am legally an adult, and I give permission 
to process my professional information for the following  
purposes:</p>"""
        
    frequencyPermission = schema.Choice(
        vocabulary=SimpleVocabulary.fromValues(
                  ['Daily','Weekly','Monthly','Seldom','Never'],
                  ),
        title = "And to send me the news:",
        required = False,
        default = 'Never',
    )    


class IGRegister (IGLogin,IHandle,IPermissions):        
   pass

class IRegister(IHandle, IEmail, IPermissions):
   pass
