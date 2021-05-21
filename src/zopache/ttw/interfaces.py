#Subject to the CV License agreement.

from zope import interface
from zope.interface import Interface
from zope import schema
from zope.schema import Password, TextLine, Int
from zope.schema import Text, TextLine, Choice, Bool, DottedName
from dolmen.container import IBTreeContainer
from cromlech.security.interfaces import IPrincipal as ICromlechPrincipal
#from cromlech.file.interfaces import IFile as IFileBase

from zopache.crud.interfaces import *
from zopache.crud.interfaces import ILeaf
from zopache.crud.interfaces import IImutable
from zopache.crud.interfaces import IMoveable
from zopache.core.interfaces import ITreeSecurity


class IMailHost(ILeaf):
    """Basic Mail CRUD"""

    postMaster = TextLine(
        title="PostMaster Email Address",
        description ="Who receives notifications.",
        default = '"John Doe" <John.Doe@mydomain.com>' ,
        required = True)

    noReply = TextLine(
        title="No Reply Email Address",
        description ="Where do the emails come from.",
        default = '"DO NOT REPLY" <noreply@yourdomain.com>' ,
        required = True)
    
    smtpServer = DottedName(
        title = u'SMTP Host Name',
        description = u'Which Mail Server are you using?',
        required = True,
    )
    
    port = Int(
        title = u'Port',
        description = u'MailHost Port Number',
        required = True,
        default = 25,
    )

    userName= TextLine(
        title = 'User Name',
        description = 'Who is the user sending the email',
        required = True,
    )

    password= TextLine(
        title = 'User Password',
        description = 'The password used to send mail.',
        required = True,
    )
    debug = Bool(
	    title = "Log Debugging Info.",
	    required = False,
	    default = False)       


class ITreeField(Interface):
      pass

vote = """Vote Permission.  After the conference I will email you 
asking you to vote on the best talks. """

oneString = """Permission to process your professional information to 
run a chat and voting server"""

from cromlech.file import FileField


class IFileBase(Interface):    
    title = TextLine(
        title = u'File Desciption',
        description = u'Describe this File.',
        required = True,
    )      
    data = FileField(title=u'Upload a File')


class IImageBase(Interface):    
    title = TextLine(
        title = u'Image Description',
        description = u'Describe this Image, so that the user has some idea what they are looking at. ',
        required = True,
    )
    remoteURL = schema.URI(
        title = "The url to visit when the image is clicked.",
        description = """The html template can use this info.. Include  'https://'""",
        missing_value="",
        required = False,
    )    
    data = FileField(title=u'Upload an Image',
                     required = False,)         

class IFile(IFileBase,ILeaf):
    pass

class IImage(IImageBase,ILeaf):
    pass

class IBTreeImage(IImage,IBTreeContainer):
    pass

class IAddBTreeImage(IImage,IBTreeContainer):
    data = FileField(title=u'Upload an Image',
                     required = True,)         
    
#I THINK ALL OD MY ZODB OBJECTS GET THIS ONE    
class ICanonical (Interface):
      pass   



class ITestURL(Interface):    
    testURL = schema.TextLine(
        title = u'Test URL',
        description = u'URL To Visit to test this script',
        required = False,
        default='/',            
    )

    

class ISupport (Interface):
    hirePermission = Bool(
	    title = "Help me to get a better job.",
	    required = False,
	    default = False)   
    hirePermission.text ="""<p>I give permission to process my professional information for the following puruposes:</p>"""

    recruitPermission = Bool(
	   title = "Help me hire a good developer / data scientist.",
	   required = False,
	 default = False)


    
class ISearchSchema(Interface):
    """Search Interface for this Principal Provider"""

    search = TextLine(
        title="Search String",
        description="A Search String",
        required=False,
        default=u'',
        missing_value=u'')



class IBranch (IBTreeContainer):
    pass

class IPrincipalFolder(ICopyable,IImutable,ICanonical):
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

class IMoveableWebClass(IWebClass,IMoveable):
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

class IAceEdit(Interface):
          pass
      
class IAceDiff(Interface):
          pass      

#NO DISPLAYALE, IT RETURNS SOME VERSION OF SOURCE
class ISourceLeaf(ISource,ILeaf,IAceEdit):
      pass


class IJavascriptIndex(Interface):
      pass

class IJavascript(ISourceLeaf,IJavascriptIndex):
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
 
class ITemplate(Interface):
    pass

   
class IJinjaJS(IJavascript,ITemplate):
    pass
    
class ISearchable(Interface):
      pass

  
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
        default = '{}',
    )

    
class IJinjaJSON(IJSON,ITemplate):
    pass

    
class ITestSource (ISource, ITestURL):
   pass

class IIndexHTML(Interface):
      pass
  
class ICkHTML (ISource):
     pass


class IAceHTML(ISource,IAceEdit,ITemplate): 
    pass

class IJinjaHTML(IAceHTML):
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

  
class IHistoricDetails(ITreeSecurity):
      pass




class IIndexHTML(Interface):
      pass


#THIS IS NOT ONLY HTML, IT IS THE HTML CLASS
#HAS TO DO WITH TRAVERSAL, AHD LOOKING UP THE VIEW

class IHTMLClass(ICkHTML, IAceHTML, IIndexHTML,ILeaf):
    pass

class IAceHTMLClass(IAceHTML, IIndexHTML,ILeaf):
    layout = schema.DottedName(
        title = u'Layout',
        max_dots=1,
         missing_value=u'',
        description = u'Renders the layout, with this html as the content.',
        required = False,
    )

class IAceCMSClass(IAceHTMLClass):
    pass

class IAceIFrameClass(IAceHTMLClass):
    pass
    
class IAceHTMLPage(IAceHTML, IIndexHTML,ILeaf):
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

class IAceContainer(IAceHTMLClass,IIndexHTML,ISourceContainer):
    pass
 
class IHTMLContainer(ISourceContainer,IHTML):
   pass

class IJavascriptFolder(IJavascript,ISourceContainer):
        "Basic Javascript Folder Form"
        pass

class IJSONContainer(IJSON, ISourceContainer):
        description= schema.Text(
        title = 'Description',
        description = """A brief introduction of this page.  
                        This is used by the search functions.""",
        required = False,
        default = u'',
    )
        
class IUntrustedHTML(IHTML):
   pass

class IUntrustedAceHTML(IAceHTML):
   pass

class IInternalPrincipal(IBTreeContainer, ICanonical,ICromlechPrincipal,IUntrustedHTML):
    """Principal information"""
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
    
class IGrapeBase(IAceHTML,IIndexHTML):
    """ For Grape Folders."""

    title = schema.TextLine(
        title = u'Title',
        description = u'Please Describe this Grape.',
        required = False,
    )

    source= schema.Text(
        title = u'JSXSource Code',
        description = u'The JSX goes here.',
        required = False,
        default = u'',
    )
    
    html= schema.Text(
        title = u'Generated HTML Source Code',
        description = u'The HTML goes here.',
        required = False,
        default = u'',
    )
    
