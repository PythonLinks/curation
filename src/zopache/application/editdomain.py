import googlemaps

from zope.interface import Interface
from zope.schema._field import Choice
from zope.schema import TextLine

from cromlech.browser.exceptions import HTTPFound

from zopache.core.viewdecorators import *
from zopache.crud.forms import EditForm
from zopache.pages.interfaces import IPage

class IDomainClass(Interface):

    domain= TextLine(
        title = 'Domain.',
        description = u'Defines the required domain for this page.',
        required = False,
        default = u'',
    )         

@form_component
@name ('editDomain')
@context(IPage)
@permissions('Manage')
class EditWebClass (EditForm):
    title = 'Edit the Domain.'
    subTitle = 'Who runs this part of the tree?'
    interface = IDomainClass
    fields = Fields(IDomainClass)
    
    
    def acquireTitle(self):
        return 'Edit' + self.context.title + "'s Domain"


