from zopache.core.viewdecorators import *

from zopache.ttw.htmlviews import (AceScripts,
                                   CkScripts,
                                   AceEditForm,
                                   CkEditForm)

from zopache.pages.htmlvalidator import HTMLValidator
from zopache.pages.interfaces import IPage
from zopache.core.interfaces import ITreeSecurity

#HERE IS THE DEVELOPER ACE EDIT FORM
@form_component
@context(IPage)
@name("aceedit")
@implementer (ITreeSecurity)
class AceEditPage(AceEditForm):
    dataValidators = [HTMLValidator]    

#HERE IS THE CKEDIT FORM
@form_component
@context(IPage)
@name('ckedit')
class CkEditPage(CkEditForm):
    dataValidators = [HTMLValidator]        



