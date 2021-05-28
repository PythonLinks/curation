from zope.interface import Interface
from zope import schema

from zopache.crud.interfaces import ILeaf,IContainer
from zopache.ttw.interfaces import ISourceLeaf
from zopache.ttw.interfaces import  IJavascriptIndex
from zopache.ttw.interfaces import ISearchable, IJavascript
from zopache.crud.interfaces import IDeletable, IMoveable,IRenameable, ICopyable

from zopache.crud.interfaces import IZMI

class IMixed(Interface):
     pass

class IPythonIndex(Interface):
     pass

class ITranscrypt(ISourceLeaf,IPythonIndex,IMixed,IJavascript,IZMI,IDeletable):
    """Basic Python  FORM with CRUD"""

    title = schema.TextLine(
        title = u'Title',
        description = u'A short reminder of what this Python code  does or its version name.',
        default='',            
        required = False,
    )

    source= schema.Text(
        title = u'Python Source Code',
        description = u'The Python code goes here.',
        required = False,
        default = u'',
    )
    
#    sideBySide = schema.Bool(
#        title = 'Side By Side',
#        description = 'Show Text Areas Side By Side?',
#        required = False,
#        default = True,
#    )       



class IPython(Interface):
    "Basic Python Form"

    title = schema.TextLine(
        title = u'Title',
        description = u'Describe this Python  Object.',
        required = False,
    )

    source= schema.Text(
        title = 'Python Source Code',
        description = u'The Python code goes here.',
        required = False,
        default = u' ',
    )
    
class IPythonScript(IPython):
    arguments = schema.TextLine(
        title = u'Arguments',
         description = 'Does this function take arguments?', 
        default='',            
        required = False,
    )     

class IDirectory(IZMI):
     pass

class IFile (Interface):
    pass

class IPythonFile(IFile,IPythonIndex):
    pass

class IJavascriptFile(IFile,IJavascriptIndex):
    pass

class IPythonFolder(IContainer,IMixed,IZMI): 
    pass

#    arguments = schema.TextLine(
#        title = u'Arguments',
#        description = u'An optional comma separated list of arguments',
#        default='',
#        required = False,
#    )    
