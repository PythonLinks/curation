from zopache.core.viewdecorators import *
from .interfaces import ISecureHTML , IWeb
from .html import Index, SecureHTML


@form_component
@name (u'index')
@context(ISecureHTML)
@title("SecureIndex")
@permissions('Manage')
@implementer(IWeb)  
class SecureIndex(Index):
     pass


from dolmen.container import IBTreeContainer
from .html import AddAceHTML 
@form_component
@name (u'addSecureHTML')
@context(IBTreeContainer)
@title("Add SecureHTML")
@permissions('Manage')
@implementer(IWeb)  
class AddSecureHTML(AddAceHTML):
    subTitle="Add a Secure HTML Object"
    factory=SecureHTML

 
