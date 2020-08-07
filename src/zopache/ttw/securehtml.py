from zopache.core.viewdecorators import *
from .interfaces import ISecureHTML , IWeb
from .html import  SecureHTML, HTMLPage
from .htmlviews import Index
from zopache.core.interfaces import ITreeSecurity

@view_component
@name (u'index')
@context(ISecureHTML)
@implementer (ITreeSecurity)
@implementer(IWeb)  
class SecureIndex(Index):
     pass

from dolmen.container import IBTreeContainer
from .htmlviews import AddAceHTML

@form_component
@name (u'addSecureHTML')
@context(IBTreeContainer)
@permissions('Manage')
class AddSecureHTML(AddAceHTML):
    subTitle="Add a Secure HTML Object"
    factory=SecureHTML


@form_component
@name (u'addHtmlPage')
@context(IBTreeContainer)
@permissions('Manage')
class AddHTMLPage(AddAceHTML):
    subTitle="Add an HTML Page"
    factory=HTMLPage

 
