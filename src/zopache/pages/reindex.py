from zopache.core.viewdecorators import *
from zopache.ttw.interfaces import IBranch
from zopache.core.baseform import Form
from zopache.ttw.interfaces import IBranch
from zopache.core.getroot import getSiteRoot, getProducts
@form_component
@context(IBranch)
@crom.target(IView)
@title("reIndex")
@crom.name("reIndex")
@permissions('Manage')
class ReIndex(Form):
    label = 'ReIndex'
    def update(self):
           root = getSiteRoot (self.context)
           root.indexTree()
           products = getProducts (self.context)
           products.indexTree()
           self.status='Branch was indexed'
           Form.update(self)

