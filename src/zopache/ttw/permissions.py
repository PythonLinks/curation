from zope.cachedescriptors.property import CachedProperty
from zopache.core.viewdecorators import *
import crom
from zopache.crud.forms import  EditForm
from zope.cachedescriptors.property import CachedProperty
from dolmen.forms.base import Actions
from cromdemo.interfaces import ITab
from .interfaces import IInternalPrincipal
from . import tal_template
from zopache.crud.actions import Update
from dolmen.forms.base import Actions
from zope.schema import Bool

class IRecruitPermissions(Interface):    
    recruitPermission = Bool(
        title = "Recruit Permission"  ,
        required = False,
        default = False)
    
    hirePermission = Bool(
        title = "Hire Permission",
        required = False,
        default = False)                         



class DoneAction (Update):
    def newURL(self,arg):
        return ('/')

@form_component
@name (u'permissions2')
@context(Interface)
@permissions('Edit')
@title("GDPR Permissions")
class Permissions(EditForm):
    """ Recruiting Permissions
    """
    title='PythonLinks.info'
    subTitle='One Last Question'
    fields = Fields(IRecruitPermissions)
    submissionError = []

    def update(self):
        root = self.getRoot()
        self.template = root['Products']['Templates']['RecruitingPermissions']
        
    @CachedProperty
    def actions(self):
        return Actions(DoneAction("Agreed",  "Agreed"),
                       DoneAction("No Thanks",  "No Thanks"))
	      
