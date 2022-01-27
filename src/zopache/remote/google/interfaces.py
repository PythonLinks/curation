from zope.interface import Interface
from zope import schema

class IGLogin(Interface):
        idtoken= schema.Text(
        title="Token",
        description= "",
        required = True)
        
class IGReg(Interface):
        idtoken= schema.ASCII(
        title="Token",
        description= "",
        required = True)        

        


class IGRegister (IGReg,IHandle,IPermissions):        
    newsPermission = schema.Bool(
        title = """ To email me the news. """,
        required = False,
        default = False)

    
   

class IGSubscribe (IGRegister):
    frequencyPermission = schema.Choice(
        vocabulary=SimpleVocabulary.fromValues(
                  ['Daily','Weekly','Monthly','Seldom','Never',''],
                  ),
        title = "To send me the news:",
        required = False,
        default = '',
    )  
