# -*- coding: utf-8 -*-

#This software is subject to the CV and Zope Public Licenses.

from cromlech.browser.interfaces import IPublicationRoot
from zope.interface import implementer, Interface
from dolmen.container import BTreeContainer,IBTreeContainer
from cromlech.browser import IView
from zope import schema
from zope.schema import Text, TextLine, Password , DottedName
from zopache.ttw.interfaces import ILeaf, IHTMLContainer
from zopache.ttw.interfaces import IHTML
from zopache.crud.interfaces import IRootContainer


class IVirtualHost(ILeaf):
    """Map domains to paths"""
    mapping = schema.Dict(
        title = u'Virtual Host Definitions',
        description = u'Map from domain names to child directory name.',
        required = False,
        key_type = DottedName(max_dots = 0) ,
        value_type = DottedName(max_dots = 0) , 
    )


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
    
#class IRootContentContainer(IRootContainer,IContentContainer):
#   pass

