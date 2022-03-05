import requests
import feedparser
from webpreview import web_preview

from dolmen.forms.base.errors import Error, Errors

from zopache.business.addbyurl import AddByURLForm
from zopache.core.viewdecorators import *
from zopache.core.interfaces import ITreeSecurity
from zopache.crud.socialmedia import SocialMediaExtractor
from zopache.pages.interfaces import IPage

@view_component
@name('addRSSByURL')
@target(IView)
@context(IPage)
@permissions('Manage')
class AddRssByURLForm(AddByURLForm):
    addSlug = "addRSS"
    title = "Add an RSS Feed"
    subTitle = "Please enter the RSS feed URL."
    datavalidators = []

    def processData(self,data):
        rssURL = data['remoteURL']
        response = {}
        errors = Errors()
        try:
           feed = feedparser.parse(rssURL)
        except Exception as error:
           title = "<h2>Error while trying to download and parse "
           title += "the RSS feed:</h2> "
           title +=  str(error)[1: -1] + ' <br>'
           title += "Pleaes check the URL of the RSS feed, and make sure "
           title += "it is working"
           errors.append(Error(title = title))
           return response, errors  
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
        if 'link' in feed:

            try:
                link = feed['link']
                remoteResponse = requests.get(link)
            except Exception as error:
               title = "<h2>The RSS feed downloaded and parsed, "
               title += "but here was an Error "
               title += "while trying to download the page. </h2>"
               title +=  str(error)[1: -1] + ' <br>'
               title += "Pleaes check the home page URL "
               title += "from the RSS feed."
               errors.append(Error(title = title))
               return response, errors  

            connect = {}
            SocialMediaExtractor().addSocialMedia(
                              connect,remoteResponse)
            if 'twitterId' in connect:
                response['form.field.twitterId'] = connect ['twitterId']
        return errors, response
