import os
from cromlech.security import permissions
from dolmen.container import IBTreeContainer
from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from here import HERE

@form_component
@context(IBTreeContainer)
@target(IView)
@name("localRestore")
@permissions('Manage')
class LocalRestore(Form):
    title = "Restore A Branch"
    subTitle = "From a file on the server. "
    def update(self):
        path = os.path.join(HERE,'data','data.import')        
        theFile = open (path,'rb')
        branch = self.context._p_jar.importFile(theFile)
        name = branch.__name__
        newName = UniqueName().uniqueContainerName(context,name)
        self.form.context [newName] = branch
        self.status = "Branch was restored"
     
