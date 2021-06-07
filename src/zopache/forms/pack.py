from cromlech.security import permissions
from zopache.core.viewdecorators import *
from zopache.ttw.interfaces import IBranch
from zopache.core.baseform import Form


@form_component
@context(IBranch)
@target(IView)
@title("Pack")
@name("pack")
@permissions('Manage')
class Pack(Form):
    label = 'Pack'
    title = "Pack the Database"
    subTitle = "This reduces the amout of disk space needed."
    def update(self):
           self.request.environ['zodb.connection'].db().pack()         
           self.status='The Database was packed'
           Form.update(self)

