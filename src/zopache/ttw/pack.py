from cromlech.security import permissions
from zopache.core.viewdecorators import *
from .interfaces import IBranch
from zopache.categories.data.youtube.getvotes import recordAllVotes
from zopache.core.baseform import Form


@form_component
@context(IBranch)
@target(IView)
@title("Pack")
@name("pack")
@permissions('Manage')
class Pack(Form):
    label = 'Pack'
    def update(self):
           self.request.environ['zodb.connection'].db().pack()         
           self.status='The Database was packed'
           Form.update(self)

