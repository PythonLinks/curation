from cromdemo.interfaces import ITab
from zopache.core.viewdecorators import *
from zopache.ttw.interfaces import IBranch
from zopache.core.baseform import Form

@form_component
@context(IBranch)
@crom.target(ITab)
@title("reIndex")
@crom.name("reIndex")
@permissions('Manage')
class ReIndex(Form):
    label = 'ReIndex'
    def update(self):
           self.context.indexTree()
           self.status='Branch was indexed'
           Form.update(self)

