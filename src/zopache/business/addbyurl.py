import json
import requests
from webpreview import web_preview

from dolmen.forms.base import Action, Actions,SuccessMarker
from dolmen.forms.base.errors import Error, Errors

from zopache.core.viewdecorators import *
from zopache.core.interfaces import ITreeSecurity
from zopache.crud.addbyurl import AddByURLForm
from zopache.crud.actions import Cancel
from zopache.crud.socialmedia import SocialMediaExtractor

#The Classes to Add
from zopache.remote.rss import RSS
from zopache.business.company import Organization
from zopache.pages.page import Link
from zopache.pages.interfaces import IPage

class ProcessURL(object):
    def processURL(self,remoteURL):
        errors = Errors()
        try:
            response = requests.get(remoteURL)
            status = response.status_code
            if status != 200: 
                raise Exception ("Status Code " + str(status))
        except Exception as err:
            error = Error("Failed to Fetch URL" + str(err))
            response = {}
            errors.append(error)            
            return response, errors
        return self.processContent(remoteURL, response)
    

@view_component
@name('addByURL')
@target(IView)
@context(IPage)
@implementer(ITreeSecurity)
class AddLinkByURL(AddByURLForm, ProcessURL):
    title = "Add a Link By URL"
    addSlug = "addLink"
    
        
    def processContent(self,remoteURL,content):        
        try:
            title, description, image  = web_preview( remoteURL, content = response.content )
        except:
            error = Error("Web Preview Failed to  Parse Response")
            return response, errors.append(error)            
        
        response = {}
        response ['form.field.remoteURL'] = remoteURL
        if title:
           response ['form.field.title']= title
        if description:
            response['form.field.description']= description
        if image:
           response ['form.field.imageURL'] = image
        return response, errors


class ProcessJSON(AddByURLForm,SocialMediaExtractor):
    def processURL(self,remoteURL):
        response = {}
        errors = Errors()
        try:
            remoteResponse = requests.get(remoteURL)
            status = remoteResponse.status_code
            if status != 200: 
                raise Exception ("Status Code " + str())
            title, description, image= web_preview(
                remoteURL, content = remoteResponse.content )
        except Exception as err:
            error = Error("Failed to Fetch and Parse URL" + str(err))
            errors.append(error)            
            return response, errors
        response = self.saveData(remoteURL,title, description, image)
        connect = response ["connect"]
        self.addSocialMedia(connect,remoteResponse)
        response = json.dumps(response)
        return {'json': response}, errors

@view_component
@name('addOrganizationByURL')
@target(IView)
@context(IPage)
class AddOrganizationByURL(ProcessJSON):
    errors = Errors()
    allowAnonymous = True
    title = "Add an Organization By URL"
    addSlug = 'addOrganization'

    def saveData(self,remoteURL, title,description,image):           
        response = {"introduction": {},
                    "content":[{}],
                    "connect": {},
                    "organization":{}
        }

        response ['connect']['remoteURL'] = remoteURL
        response ['content'][0]['title']= title
        response['content'][0]['description']= description
        response ['introduction']['imageURL'] = image
        return response


@view_component
@name('addOnlineOrganizationByURL')
@target(IView)
@context(IPage)
class AddOnlineOrganizationByURL(AddOrganizationByURL):
    allowAnonymous = True
    title = "Add an Online Organization By URL"
    addSlug = 'addOnlineOrganization'


    
@view_component
@name('addCandidateByURL')
@target(IView)
@context(IPage)
class AddCandidateByURL(ProcessJSON ):
    allowAnonymous = True
    title = "Add a Candidate By URL "
    subTitle = "Just submit the URL for the candidate. "
    addSlug = 'addCandidate'        

    def saveData(self,remoteURL, title,description,image):
        response = {"introduction": {}, 
                    "content":{"english":{}},
                    "connect": {},
                    "organization":{},
                    "candidateInfo":{}
        }

        response ['connect']['remoteURL'] = remoteURL

        if title:
            response ['introduction']['title']= title
        
        if description:
            response['content']['english']['description']= description
            
        if image:
            response ['introduction']['logoURL'] = image
        return response
