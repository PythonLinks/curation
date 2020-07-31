# -*- coding: utf-8 -*-

#This software is subject to the CV and Zope Public Licenses.

from cromlech.browser.interfaces import IPublicationRoot
from zope.interface import implementer, Interface
from dolmen.container import BTreeContainer,IBTreeContainer
from cromlech.browser import IView
from zope import schema
from zope.schema import Text, TextLine, Password , DottedName
from zopache.crud.interfaces import IEditable
from zopache.ttw.interfaces import ILeaf, IHTMLContainer
from zopache.ttw.interfaces import IHTML
from zopache.crud.interfaces import IImutable
from zopache.zmi.interfaces import IZMI
from zopache.crud.interfaces import IZodbRoot

#The Root Container also has to implement IPublicationRoot      
#But you cannot delete or rename the root container
#So no IDeletable or IRenameable
class IRootContainer(IPublicationRoot,IImutable,IZMI,IZodbRoot):
     pass

class IEditableRootContainer(IRootContainer, IEditable):
      pass

class ILogin(Interface):
    email = TextLine(
        title='Username', required=True)

    password = Password(
        title='Password', required=True)
    
class IContent(ILeaf,IHTML):
   pass

class IContentContainer(IHTMLContainer):
    pass

class IChat(IHTMLContainer):
    pass
    


