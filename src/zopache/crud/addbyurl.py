from urllib.parse import urlencode

from webpreview import web_preview
from dolmen.forms.base.markers import FAILURE
from dolmen.forms.base import Action, SuccessMarker
from dolmen.forms.base.errors import Error, Errors
from dolmen.forms.base import Action, Actions,SuccessMarker

from zopache.crud.actions import Cancel
from zopache.crud.forms import AddFormBase
from .interfaces import IURLForm
from zopache.forms.urlvalidator import DuplicateURLValidator

class AddByURLAction(Action):
    """Do not create, just crawl and redirect
    """
    
    def __call__(self, form):
        self.form=form
        data, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE
        remoteURL = data["remoteURL"]
        response = form.processURL(remoteURL)
        baseURL = '/' + form.context.__name__
        postingURL = (baseURL + '/' + form.addSlug + 
                      "?" +
                      urlencode(response))
        return SuccessMarker('Updated', True, url=postingURL)
        
    
class AddByURLForm(AddFormBase):
    
    datavalidators = [DuplicateURLValidator]
    
    preamble = """This form may take a few moments  to process. 
    The software will download that webpage, capture the title, 
    description and the image url, amd you will then be redirected to the 
    real add form, but the fields will be prepopulated, saving you a lot of 
    work.  Often the Title will need to be changed, to make it more 
    relevant to this site. Sometimes the description will also need to 
    be edited """
    actions = Actions()

    title = "Add an object starting with its URL."
    @property 
    def subTitle(self):
        return f"""To a {self.contextClassName()} called 
{self.context.title}
"""
    
    def update(self):
        if self.isPerson() and not self.treeSecurity():
            self.raiseUnauthorized()
        self.addUnauthorizedActions()
            
    interface = IURLForm
    actions = Actions()
    
    def addAuthorizedActions(self):   
        actions = Actions(
                   AddByURLAction("Add"),
                   Cancel("Cancel"))
        self.actions= actions

    def addUnauthorizedActions(self):
       self.addAuthorizedActions()

