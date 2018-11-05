# -*- coding: utf-8 -*-

#This software is subject to the CV and Zope Public Licenses.

from cromlech.browser.interfaces import IPublicationRoot
from zope.interface import implementer, Interface
from dolmen.container import BTreeContainer,IBTreeContainer
from cromlech.browser import IView
from zope.schema import Text, TextLine, Password
from zopache.ttw.interfaces import ILeaf, IHTMLContainer
from zopache.ttw.interfaces import IHTML
from zopache.crud.interfaces import IRootContainer

class ITab(IView):
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
    
class IRootContentContainer(IRootContainer,IContentContainer):
   pass

