#Subject to the CV License agreement.

from zope import interface
from zope.interface import Interface
from zope import schema
from zope.schema import Password, TextLine
from zope.schema import Text, TextLine, Choice, Bool, DottedName
from z3c.schema.email  import RFC822MailAddress as Email
from dolmen.container import IBTreeContainer
from cromlech.security.interfaces import IPrincipal as ICromlechPrincipal
from cromlech.file.interfaces import IFile as IFileBase

from zopache.crud.interfaces import *
from zopache.crud.interfaces import ILeaf
from zopache.crud.interfaces import IImutable
from zopache.crud.interfaces import IMoveable

class ITreeField(Interface):
      pass


vote = """Vote Permission.  After the conference I will email you 
asking you to vote on the best talks. """

oneString = """Permission to process your professional information to 
run a chat and voting server"""

from cromlech.file import FileField

class IFile(IFileBase,ILeaf):
         data = FileField(title=u'Upload a File')

class IImage(IFileBase,ILeaf):
         data = FileField(title=u'Upload an Image')         

class ICanonical (Interface):
      pass   
    
class ITestURL(Interface):    
    testURL = schema.TextLine(
        title = u'Test URL',
        description = u'URL To Visit to test this script',
        required = False,
        default='/',            
    )






    
class IGLogin(Interface):
        idtoken= Text(
        title="Token",
        description= "A Google Login Token",
        required = True)
        

class IPermissionsBase (Interface):

    handle = DottedName(
        title="User Name",
        description= "You can log in with this.  No spaces.",
        required = True)

    email = Email(
        title="Your Email Address",
        description ="",

        required = True)
    
    password = Password(
        title="Password",
        description = "Be Strong",
        required = True)

    
class ISharedShort(Interface):        

    chatPermission = Bool(
        title = "Run this web server.",
        required = True,
        default = False)

    
class IShared(Interface):            
    newsPermission = Bool(
        title = "Please recommend good videos.",
        required = False,
        default = False)    

    hirePermission = Bool(
	    title = "Help me to get a better job.",
	    required = False,
	    default = False)   

    recruitPermission = Bool(
	   title = "Help me hire a good developer / data scientist.",
	   required = False,
	 default = False)



class ExtrePermissions(Interface):
    """    
    pugPermission =Bool(
	 title = "Pug course permissions.",
	 required = False,
	 default = False)

    pyodidePermission =Bool(
	 title = "PyOdide course permissins",
	 required = False,
	 default = False)

    helpPermission =Bool(
	 title = "Help curate content",
	 required = False,
	 default = False)    
    """              
    
class IPermissions (IPermissionsBase,IShared):    
    pass

class IPermissionsShort (IPermissionsBase,ISharedShort):    
    pass

class IGRegister (ISharedShort):        
    idtoken= Text(
                 title="Token",
                 description= "A Google Login Token",
                 required = True)


class IRegister(IPermissions):
   pass

class IRegisterShort(IPermissionsShort):
   pass

    
class ISearchSchema(Interface):
    """Search Interface for this Principal Provider"""

    search = TextLine(
        title="Search String",
        description="A Search String",
        required=False,
        default=u'',
        missing_value=u'')

class IInternalPrincipal(IFile,IContainer, ICanonical,ICromlechPrincipal):
    """Principal information"""
    pass

class ILogin(Interface):

    email  = TextLine(
        title='Username', required=True)

    password = Password(
        title='Password', required=True)

class IBranch (IBTreeContainer):
    pass

class IPrincipalFolder(IImutable):
    pass

#    def getIdByEmail(self,email):
#        """Return the principal id currently associated with login.
       
#        KeyError is raised if no principal is associated with email.

#        """
    
    #def getIdBySlugifiedHandle(self,handle):
#        """Return the principal id currently associated with handle.

#        KeyError is raised if no principal is associated with handle.

#        """        
    #Cromlech does not yet support the following. 
    #contains(IInternalPrincipal)

#BTREE CONTAINERS ARE NOT MUTABLE
#Basically these 3 are not moveable, deletable, renamable,
#editale, or anything.


class IWebClass(IImutable, ICanonical):
    pass

class IMutableWebClass(IWebClass,IContainer):
    pass

class IProducts(IBranch,IWebClass):
    pass

class ISource(ILeaf):      

    title = schema.TextLine(
        title = u'Version Name:',
        description = u'Describe this HTML Page.',
        required = False,
    )

    source= schema.Text(
        title = u'Source:',
        description = u'This is the text which defines the HTML.',
        required = False,
        default = u'',
    )


#NO DISPLAYALE, IT RETURNS SOME VERSION OF SOURCE
class ISourceLeaf(ISource,ILeaf):
      pass

class IPython(ISourceLeaf,ITestURL):
    """Basic Python  FORM with CRUD"""
    arguments = schema.TextLine(
        title = u'Arguments',
        description = u'An optional comma separated list of arguments',
        default='',
        required = False,
    )    
    
    source= schema.Text(
        title = u'Python Source Code',
        description = u'The Python code goes here.',
        required = False,
        default = u'',
    )
    title = schema.TextLine(
        title = u'Title',
        description = u'A short reminder of what this Python code  does or its version name.',
        default='',            
        required = False,
    )

class IJavascript(ISourceLeaf):
    "Basic Javascript Form"

    title = schema.TextLine(
        title = u'Title',
        description = u'Describe this Javascript Object.',
        required = False,
    )

    source= schema.Text(
        title = u'Javascript Source Code',
        description = u'The Javascript code goes here.',
        required = False,
        default = u' ',
    )


class IJSON(IJavascript):
    """Basic JSON CRUD """

    title = schema.TextLine(
        title = u'Title',
        description = u'Please Describe this JSON.',
        required = False,
    )

    source= schema.Text(
        title = u'JSON Source',
        description = u'The JSON  goes here.',
        required = False,
        default = u'',
    )
    
class ITestSource (ISource, ITestURL):
   pass

class IIndexHTML(Interface):
      pass
  
class ICkHTML (ISource):
     pass

class IAceHTML(ISource): 
    pass

class ISecureHTML(IAceHTML):
    pass

class IHTML (ICkHTML,IAceHTML,ISource):
      pass

#Views that are in the web menu. 
class IWeb(Interface):
      pass


#Views that are in the web menu. 
class IWeb(Interface):
      pass

class IHistoryItem(Interface):
      pass

class IHistoricDetails(Interface):
      pass




class IIndexHTML(Interface):
      pass


#THIS IS NOT ONLY HTML, IT IS THE HTML CLASS
#HAS TO DO WITH TRAVERSAL, AHD LOOKING UP THE VIEW

class IHTMLClass(ICkHTML, IAceHTML, IIndexHTML,ILeaf):
    pass

class IAceHTMLClass(IAceHTML, IIndexHTML,ILeaf):
    pass

  
#A COUNTAINER WITHOUT DISPLAYABLE
# RETURNS SOME VERSION OF SOURCE
#THIS IS USED BY JAVASCRIPT CONTAINERS
#AND HTML CONTAINERS
class ISourceContainer(ISource,
                    IBTreeContainer,
                    IAddContainer,
                    IRenameable,
                    ICopyable,
                    IMoveable,
                    IDeletable
               ): 
     pass

class IHTMLContainer(ISourceContainer,IHTML):
   pass



class IUntrustedHTML(IHTML):
   pass


#This file is copied from my production servers.
#The stuff after this line is not yet needed for the
#pulic zopache release. 
"""

class ISimpleBranch(Interface):
    title = schema.TextLine(
        title = u'Title',
        description = u'Title for this Branch.',
        required = False,
    )



class ITTWPrincipalFolder(Interface):
    pass



class IZopache(Interface):
    pass

"""
