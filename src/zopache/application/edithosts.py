from dolmen.forms.base import Fields

from zopache.core.viewdecorators import *
from zopache.application.interfaces import IRootContainer    
from zopache.core.interfaces import ITreeSecurity
from zopache.ttw.JSON import AceEditJSON
from zopache.ttw.htmlviews import AceEditForm
from zopache.application.validate import VirtualHostValidator
from zopache.ttw.interfaces import IJSON

@form_component
@context(IRootContainer)
@name("aceedit")
@implementer(ITreeSecurity)
class AceEditJSON(AceEditJSON):
    subTitle='Edit the Virtual Hosts'    
    datavalidators = [VirtualHostValidator]
    interface = IJSON

    @property
    def fields(self):
        return  Fields(self.interface)


