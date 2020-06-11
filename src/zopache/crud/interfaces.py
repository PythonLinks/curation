# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.

from cromlech.browser.interfaces import IPublicationRoot
from zope.interface import Interface, Attribute
from zope import schema
from zope.schema import TextLine, Text,  DottedName
from dolmen.container.interfaces import IBTreeContainer
from zopache.zmi.interfaces import IZMI


class IZodbRoot(Interface):
    pass

#Views that are in the app menu.
#That menu is to be modified by users/developers. 
class IApp(Interface):
      pass

class IName(Interface):
      __name__ = TextLine(
           title=(u"URL Segment Name (required)"),
           description = """This is the text string that shows up in the url.  
These characters include digits (0-9), letters(A-Z, a-z), and a few special characters ( "-" , "." , "_" , "~" ).  If you use other characters, they 
will be made web-safe.""", 
           required=True,
           default=None)

class IURLForm(Interface):
    title = schema.TextLine(
        title = u'Page Name',
        description = u'Describe this page.',
        required = True,
    )
    
    remoteURL= schema.URI(
        title = 'URL',
        description = 'The url of the remote web page',
        required = True,
    )      

#Objects which can be deleted.  You cannot delte the root object. 
class IDeletable(Interface):
      pass

#Objects which can be edited.  
class IEditable(Interface):
    pass

#Objects which can be displayed
class IDisplayable(Interface):
     pass

#Objects which can be renamed.  You cannot rename the root object. 
class IRenameable(Interface):
     pass

class IMoveable(Interface):
      pass

class ICopyable(Interface):
      pass

#Objects to which you can add stuff.  You cannot add stuff to leaves.  
class IAddContainer(Interface):
     pass

class IZMI(IRenameable,
                 IMoveable,
                 ICopyable,
                 IDeletable
          ):
      pass

#Not HTML
class IContainer(IZMI,
                 IBTreeContainer,
                 IAddContainer
                 ): 
     pass

class IEditableContainer(IContainer,IEditable):
          pass
 
class IImutable(     IBTreeContainer,
                     IZMI,
                     IAddContainer,
                     IDisplayable,
                     ):
      pass

class IEditableImutable(IImutable,IEditable):
    pass
      
      

#The Root Container also has to implement IPublicationRoot      
#But you cannot delete or rename the root container
#So no IDeletable or IRenameable
class IRootContainer(IPublicationRoot,IImutable,IZMI,IZodbRoot):
     pass

class IEditableRootContainer(IRootContainer, IEditable):
      pass

#You cannot add things to a leaf.    
class ILeaf(IRenameable,
            IDisplayable,
            IDeletable,
                 IMoveable,
                 ICopyable):
      pass

class IEditableLeaf(ILeaf,IEditable):
      pass
