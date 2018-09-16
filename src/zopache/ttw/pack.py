from cromlech.security import permissions
from crom import target, order
from cromdemo.interfaces import ITab
from cromlech.browser.directives import title
from dolmen.forms.base import action, name, context, form_component
from .interfaces import IBranch
from zopache.categories.data.youtube.getvotes import recordAllVotes
from zopache.core.baseform import Form


@form_component
@context(IBranch)
@target(ITab)
@title("Pack")
@name("pack")
@permissions('Manage')
class Pack(Form):
    label = 'Pack'
    def update(self):
           self.request.environ['zodb.connection'].db().pack()         
           self.status='The Database was packed'
           Form.update(self)

