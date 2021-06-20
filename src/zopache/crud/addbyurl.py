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
        response = self.processURL(remoteURL,form)
        baseURL = '/' + form.context.__name__
        postingURL = (baseURL + '/' + form.addSlug + 
                      "?" +
                      urlencode(response))
        return SuccessMarker('Updated', True, url=postingURL)
        
    def processURL(self,remoteURL,form):
        try:
            result = web_preview(remoteURL, parser="html.parser")
        except:
            error = Error("Failed to Fetch and Parse URL")
            return Errors().append(error)
        
        response = {}
        response ['form.field.remoteURL'] = remoteURL
        response ['form.field.title']= result[0]
        response['form.field.description']= result[1]
        response ['form.field.imageURL'] = result[2]
        return response

import feedparser
class AddFeedByURLAction(AddByURLAction):
    addSlug = "addRSS"
    def processURL(self,rssURL,form):
        try:
           feed = feedparser.parse(rssURL)

        except:
            error = Error("Failed to Fetch and Parse Feed")
            return Errors().append(error)
        
        feed = feed.feed
        response = {}
        response ['form.field.rssURL'] = rssURL
        if 'link' in feed:
            response ['form.field.remoteURL'] = feed.link
        if 'title' in feed:             
            response ['form.field.title']= feed.title
        if 'description' in feed:
            response['form.field.description']= feed.description
        if 'image' in feed:
            if 'href' in feed.image:     
               response ['form.field.logoURL'] = feed.image.href
        return response       
    
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
    
    def addUnauthorizedActions(self):   
        actions = Actions(
                   AddByURLAction("Add"),
                   Cancel("Cancel"))
        self.actions= actions
              

