from zopache.core.viewdecorators import *
from zopache.application.interfaces import IRootContainer    
from zopache.core.interfaces import ITreeSecurity
from zopache.ttw.JSON import AceScripts
from zopache.ttw.htmlviews import AceEditForm
from zopache.application.validate import VirtualHostValidator
@form_component
@context(IRootContainer)
@name("aceedit")
@implementer(ITreeSecurity)
class AceEditJSON(AceScripts,AceEditForm):
    subTitle='Edit the Virtual Hosts'    
    datavalidators = [VirtualHostValidator]

