
#CURRENTLY JUST TO A SINGLE PERSON
#CURRENTLY ONLY USES MAIL QUEUE

from zope import schema

from zopache.core.viewdecorators import *
from zopache.core import Leaf
from zopache.crud.interfaces import ILeaf
from zopache.pages.interfaces import IRootPage
from zopache.crud.forms import AddNamedForm, EditForm
from zopache.application.interfaces import IVirtualHost

    

@implementer (IVirtualHost)
class VirtualHost(Leaf):
    title = "Virtual Host Definitions" 
    pass

    
@form_component
@name('addVirtualHost')
@context(IRootPage)
@permissions('Manage')
class AddHost(AddNamedForm):
    subTitle='Add a Virtual Host'
    interface = IVirtualHost
    ignoreContent = True
    factory=VirtualHost
    def newName(self,data):
        return "VirtualHost"
    
#HERE IS THE  EDIT FORM
@form_component
@context(IVirtualHost)
@name("edit")
@permissions('Manage')
class EditHost(EditForm):
    subTitle='Edit the VirtualHost Object'    
