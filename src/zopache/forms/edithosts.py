from zope.interface import Interface
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema import TextLine, Dict


class IVirtualHosts(Interface):
         
    virtualHosts = Dict (
        key_type = TextLine(),
        value_type = TextLine(),
        title="Virtual Hosts",
        description= "Map from domain name to Folder.",
        required = False)                
    

from zopache.core.viewdecorators import *
from zopache.crud.interfaces import  IZodbRoot
from zopache.crud.forms import EditForm

@form_component
@name ('editHosts')
@context(IZodbRoot)
@permissions('Manage')
class EditPermissions (EditForm):
    title = 'Edit The Virtual Hosts'
    suTitle = 'Map from domain to Folder.'
    interface = IVirtualHosts
    fields = Fields(IVirtualHosts)
        
    def acquireTitle(self):
        return 'Edit Permissions'

    def updateWidgets(self):
        super().updateWidgets()
        pass
