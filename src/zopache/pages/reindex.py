from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.ttw.interfaces import IBranch
from zopache.core.getroot import getSiteRoot, getProducts
from zopache.ttw.interfaces import IWebClass

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
           if hasattr(root, 'indexTree'):
              root.indexTree()
           products = getProducts (self.context)
           products.indexTree()
           self.status='The tree of pages was indexed'
           Form.update(self)

