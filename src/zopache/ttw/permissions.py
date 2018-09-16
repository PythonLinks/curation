from zopache.core.viewdecorators import *
from zopache.crud.forms import EditForm
from .interfaces import IInternalPrincipal
from .interfaces import IPermissions


@form_component
@name (u'permissions')
@context(IInternalPrincipal)
@title("GDPR Permissions")
class Permissions(EditForm):
    """ Recruiting Permissions
    """
    title='PythonLinks.info'
    subTitle=''
    fields = Fields(IPermissions)
    ignoreContent = True
    submissionError = []

    def nextURL(self):
        return "."            





 
