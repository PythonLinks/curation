from zopache.core.viewdecorators import *
from zopache.ttw.interfaces import IBranch
from zopache.core.baseform import Form
from zopache.ttw.interfaces import IBranch
from zopache.core import getRoot
@form_component
@context(IBranch)
@crom.target(IView)
@title("reIndex")
@crom.name("reIndex")
@permissions('Manage')
class ReIndex(Form):
    label = 'ReIndex'
    def update(self):
           root = getRoot (self.context)
           root.indexTree()
           root['Products'].indexTree()
           self.status='Branch was indexed'
           Form.update(self)

