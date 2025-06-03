from cromlech.security import permissions
from dolmen.container import IBTreeContainer
from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.remote.postalcodes.read import createCodes

@form_component
@context(IBTreeContainer)
@target(IView)
@name("loadZip")
@permissions('Manage')
class Clean(Form):
    title = "Load zip codes"
    subTitle = ""
    def update(self):
           createCodes(self.context)
           self.status='The zip codes were loaded'
           Form.update(self)

