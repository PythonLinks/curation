from zope.interface import Interface
from zope.schema._field import Choice
from zope.schema import Text, TextLine, Bool

from cromlech.browser.exceptions import HTTPFound

from zopache.core.viewdecorators import *
from zopache.crud.forms import EditForm
from zopache.pages.interfaces import IPage
from zopache.forms.interfaces import IApprove

@form_component
@name ('approve')
@context(IPage)
class Approve (EditForm):
    title = 'Aprove this posting'
    subTitle = ''
    interface = IApprove
    fields = Fields(IApprove)
    

