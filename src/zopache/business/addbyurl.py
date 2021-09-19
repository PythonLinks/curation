#ADD LINK
import requests

from dolmen.forms.base import Action, Actions,SuccessMarker
from zopache.core.viewdecorators import *
from zopache.core.interfaces import ITreeSecurity
from zopache.crud.addbyurl import AddByURLForm
from zopache.crud.actions import Cancel
#The Classes to Add
from zopache.remote.rss import RSS
from zopache.business.company import Organization
from zopache.pages.page import Link
from zopache.pages.interfaces import IPage
from html_to_etree import parse_html_bytes
from webpreview import web_preview

@view_component
@name('addByURL')
@target(IView)
@context(IPage)
@implementer(ITreeSecurity)
class AddLinkByURL(AddByURLForm):
    title = "Add a Link By URL"
    addSlug = "addLink"
    
    def processURL(self,remoteURL):
        try:
            response = requests.get(remoteURL)
        except:
            error = Error("Failed to Fetch URL")
            return Errors().append(error)
        
        try:
            title, description, image  = web_preview( remoteURL, content = response.content )
        except:
            error = Error("Web Preview Failed to  Parse Response")
            return Errors().append(error)            
        
        response = {}
        response ['form.field.remoteURL'] = remoteURL
        response ['form.field.title']= title
        response['form.field.description']= description
        response ['form.field.imageURL'] = image
        return response

import feedparser    
@view_component
@name('addRSSByURL')
@target(IView)
@context(IPage)
@permissions('Manage')
class AddRssByURLForm(AddByURLForm):
    addSlug = "addRSS"
    title = "Add an RSS Feed"
    datavalidators = []

    def processURL(self,rssURL):
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

def addToConnect(connect,pattern,key,url):
    if pattern in url:
       connect[key] = url
                 
@view_component
@name('addOrganizationByURL')
@target(IView)
@context(IPage)
class AddOrganizationByURL(AddByURLForm):
    allowAnonymous = True
    title = "Add an Organization By URL"
    addSlug = 'addOrganization'

    def processURL(self,remoteURL):
        try:
            remote = requests.get(remoteURL)
            title, description, image= web_preview(
                remoteURL, content = remote.content )
        except:
            error = Error("Failed to Fetch and Parse URL")
            return Errors().append(error)

        response = self.saveData(remoteURL,title, description, iamge)
        connect = response ["connect"]
        self.addSocialMedia(connect,remotePage)
        return response
    
    def saveData(self,remoteURL, title,description,image):           
        response = {introduction: {},
                    content:[],
                    connect: {},
                    organization:{}
        }

        response ['connect']['remoteURL'] = remoteURL
        response ['content'][0]['title']= title
        response['content'][0]['description']= description
        response ['introduction']['imageURL'] = image
        return response

    def addSocialMedia (self, connect, remotePage): 
        tree = parse_html_bytes(remotePage.content, remotePage.headers.get('content-type'))
        socialMedia = set(find_links_tree(tree))        
        for link in socialMedia:
           if 'facebook.com' in link:
               if 'facebook.com/group' in link:
                  connect['facebookGroup'] = link
               else:
                  connect['facebookPage'] = link
           if 'twitter.com/' in link:
               parts = link.split('twitter.com/')
               connect['twitterId'] = parts[1]

           addToConnect(connect,'instagram.com','instagramURL', link)
           addToConnect(connect,'youtube.com','youtubeChannelURL', link)
           addToConnect(connect,'vimeo.com', 'vimeoURL', link)

    
@view_component
@name('addCandidateByURL')
@target(IView)
@context(IPage)
class AddCandidateByURL(AddByURLForm):
    allowAnonymous = True
    title = "Add a Candidate By URL "
    subTitle = "Just submit the URL for the candidate. "
    addSlug = 'addCandidate'        

    def saveData(self,remoteURL, title,description,image):           
        response = {introduction: {}, 
                    content:[],
                    connect: {},
                    organization:{},
                    candidateInfo:{}
        }

        response ['connect']['remoteURL'] = remoteURL
        response ['content']['english']['title']= title
        response['content']['english']['description']= description
        response ['introduction']['imageURL'] = image
        return response
