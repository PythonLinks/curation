from zopache.core.viewdecorators import *
from zopache.ttw.interfaces import IBranch
from zopache.core.baseform import Form
from zopache.pages.interfaces import IRootPage

@form_component
@context(IRootPage)
@crom.target(IView)
@title("reIndex")
@crom.name("reIndex")
@permissions('Manage')
class ReIndex(Form):
    label = 'ReIndex'
    def update(self):
           self.context.indexTree()
           self.status='Branch was indexed'
           Form.update(self)

