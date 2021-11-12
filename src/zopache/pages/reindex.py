from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.ttw.interfaces import IBranch
from zopache.ttw.interfaces import IWebClass

@form_component
@context(IBranch)
@crom.target(IView)
@crom.name("reIndex")
@permissions('Manage')
class ReIndex(Form):
    label = 'ReIndex'
    def update(self):
           root = self.getSiteRoot ()
           products = self.getProducts ()
           products.indexTree()
           people = self.getPrincipalFolder()
           people.indexTree()
           self.status='The tree of pages was indexed'
           Form.update(self)

