# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.
import requests
from slugify import slugify, SLUG_OK

from webpreview import web_preview

from zope.event import notify
from zope.location import ILocation
from zope.lifecycleevent import ObjectCreatedEvent
#https://github.com/ludbek/webpreview
from webpreview import web_preview
import requests
from html_to_etree import parse_html_bytes
#https://github.com/fluquid/extract-social-media
from extract_social_media import matches_string, find_links_tree

from cromlech.browser import IURL
from dolmen.forms.base import Action, SuccessMarker
from dolmen.forms.base.markers import FAILURE
from dolmen.forms.base.utils import set_fields_data, apply_data_event
from cromlech.browser.exceptions import HTTPFound
from dolmen.forms.base.errors import Error, Errors
from zopache.core.getroot import getSiteRoot
from zopache.crud import i18n as _
from zopache.core.uniquename import UniqueName
from zopache.core.transactionnote import TransactionNote
from zopache.ttw.file import BTreeImage

class Cancel(Action):
    """Cancel the current form and return on the default content view.
    """

    def __call__(self, form):
        content = form.getContentData().getContent()
        url = str(IURL(content, form.request))
        return SuccessMarker('Aborted', True, url=url)

class View(Action):
    """ View the object.
    """

    def __call__(self, form):
        content = form.getContentData().getContent()
        url = str(IURL(content, form.request))
        return SuccessMarker('Aborted', True, url=url)    

from PIL import Image as PilImage
from io import BytesIO
class Add(Action, UniqueName, TransactionNote):
    """Add action for an IAdding context.
    """
    def appendName(self,url,name):
        return url + "/" + name
    
    def __init__(self, title, factory):
        Action.__init__(self,title)
        self.factory = factory


    def __call__(self, form):
        self.form=form
        obj= form.factory()
        self.new=form.new=obj

        data, errors = self.form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE
        self.data = data
        errors = self.setFields()
        if errors:
            form.submissionError = errors
            return FAILURE        
        return self.callInner(obj,data,form)
    
    def baseURL(self):
        return self.form.absoluteURL (self.new)
        
    def callInner(self,obj,data,form):     
        notify(ObjectCreatedEvent(obj))
        self.actuallyAdd(obj,data)
        form.message("Content created")
        baseURL = self.baseURL()
        print ("IN ADD", baseURL)
        self.describeWithView(obj,form)

        #NOW DO Form Specific newURLs. 
        if hasattr(form, 'newURL'):
           url=self.form.newURL(baseURL)
        else:
           url=self.newURL(baseURL)
        #Form Specific postAddProcessing
        if hasattr(form,'postAddProcess'):
               form.postAddProcess()
        elif hasattr(form.new,'postAddProcess'):
               form.new.postAddProcess(view=form)

        #Now do form specific returns
        
        #DISCORD USES THIS, DOES NOT REDIRECT
        if hasattr(form,'getReturn'):
            return form.getReturn(url)
        else:
           return SuccessMarker('Added', True, url=url,code=307)
    
    def setFields(self):
            set_fields_data(self.form.fields, self.new, self.data)
            return Errors()

    def getName(self,data):
        if hasattr(self.form, 'newName'):
           newName = self.form.newName(data)
        else:   
           newName = self.newName(data)
        return newName
    
    def actuallyAdd(self,item,data):
        newName = self.getName(data)
        context = self.form.context   
        context[newName]=item
        item.__parent__ = context
        
    def newURL(self,baseURL):
        if hasattr(self.form, 'newURL'):
            return self.form.newURL(baseURL)
        else:
            return baseURL

    def newName(self,data):
        name =  data['__name__']        
        return self.uniqueContainerName(self.form.context,name)

    def setImage(self,imageURL):
        try:
            response = requests.get(imageURL)            
            zodbImage =BTreeImage()
            zodbImage.contentType=response.headers['content-type']            
            content = response.content
            zodbImage.data = content
            pilImage = PilImage.open(BytesIO(content))
            zodbImage.width = pilImage.width
            zodbImage.height = pilImage.height
            new = self.form.new
            new['Logo']= zodbImage
            zodbImage.__parent__ = new
        except:
            pass 
                     
class AddNamed(Add):
    pass

class AddByTitle (Add):
    def actuallyAdd(self,item,data):
        newName = self.newName(data)
        context = self.getContext(data)
        context[newName]=item
        item.__parent__ = context
        item.__name__ = newName
        root = getSiteRoot(self.form.context)
        if hasattr(root,'addItem'):
            root.addItem(self.new)

        if hasattr(self.new,'imageURL'):
            self.setImage (self.new.imageURL)
            del self.new.imageURL
            
    def baseURL(self):
        result = "/" + self.form.urlEncode(self.new.__name__)
        return result
    
    def getContext(self,data):
        return self.form.context
    
    def newName(self,data):    
        newName =  data['title']
        return self.uniqueBothName(self.form.context,newName)

class AddByTitleAndCkEdit(AddByTitle):    
    def newURL(self,baseURL):
        return baseURL + '/ckedit'
    
class AddByTitleAndAceEdit(AddByTitle):    
    def newURL(self,baseURL):
        return baseURL + '/aceedit'    

class NotUsed():
    def extractSocialMediaLinks(self,response):
         tree = parse_html_bytes(response.content,
                    response.headers.get('content-type'))
         links = set(find_links_tree(tree))
         remainingLinks = []
         
         for url in links:
             if 'facebook.com/group/' in url:
                 self.processURL(self,url,'facebookGroup',
                                 'acebook.com/group/')
                 continue
             if 'facebook.com/' in url:
                  self.processURL(self,url,'facebookId',
                                 'acebook.com/')
                  continue
             if 'twitter.com/' in url:  
                  self.processURL(self,url,'twitterId',
                                 'witter.com/')
                  continue              
             if 'twitter.com/intent/follow?screen_name=' in url:  
                  self.processURL(self,url,'twitterId',
                    'witter.com/intent/follow?screen_name=')
                  continue
             if 'twitter.com/' in url:  
                  self.processURL(self,url,'twitterId',
                                 'witter.com/')
                  continue              
             if 'youtube.com/channel' in url:  
                  self.processURL(self,url,'youtubeId',
                                 'youtube.com/channel/')
                  continue
             if 'youtube.com/user' in url:  
                  self.processURL(self,url,'youtubeId',
                                 'youtube.com/user/')
                  continue
             if 'youtube.com/' in url:  
                  self.processURL(self,url,'youtubeId',
                                 'youtube.com/')
                  continue                            
             if 'instagram.com/' in url:  
                  self.processURL(self,url,'instagramId',
                                 'stagram.com/')
                  continue
             remainingLinks.append(url)
                 
         allLinks = []       
         for item in remainingLinks:                                
              oneLink = self.href(item,item)
              allLinks.append(oneLink)                    
              self.new.source = '<br>'.join(allLinks)

class AddByTitleToTreeAndView(AddByTitle):

    def getContext(self,data):
        if not 'categoryName' in data:
            return self.form.context
        siteRoot = self.form.getSiteRoot()
        categoryName = data ['categoryName']
        category = siteRoot [categoryName]
        return category
    
    def setFields(self):
            set_fields_data(self.form.fields, self.new, self.data)
            return Errors()
    
class AddAndView(AddNamed):
    def newURL(self,baseURL):
        return baseURL + '/index'        
    
class Update(Action,TransactionNote):
    """Update action for any locatable object.
    """

    def __call__(self, form):
        self.form=form
        data, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE
        apply_data_event(form.fields, form.getContentData(), data)
        form.message(_(u"URL updated"))
        breakpoint()        
        if hasattr(form,'postProcess'):        
               form.postProcess(view = form)
        elif hasattr(form.context,'postProcess'):
               form.context.postProcess(view=form)
        baseURL = self.form.absoluteURL()
        url=self.newURL(baseURL)
        self.describeWithView(form.context,form)
        if url == form.request.url:
           return SuccessMarker('Updated', True)
        else:
           return SuccessMarker('Updated', True, url=url)

    def appendName(self,baseURL,name):
        if baseURL == "":
           baseURL = "/"
        elif baseURL [-1] != "/":
            baseURL += "/"
        baseURL += name
        return baseURL

    def newURL(self,baseURL):
        if hasattr(self.form, 'newURL'):
            return self.form.newURL(baseURL)
        else:
           result = self.appendName(baseURL,getattr(self.form,"crom.name"))
           return result

    def postProcess(self):
            pass

from zopache.business.interfaces import IOrganization
from bs4 import BeautifulSoup
class AddByCrawl(Add):
    fields = IOrganization
    def __call__(self, form):
        self.form = form
        self.data = form.request['form.field.data']

        soup = BeautifulSoup(self.data, 'html.parser')
        divs = soup.findAll("div", {"class": "views-rows"})
        for item in divs:
            new = form.factory
            new.imageURL = item.img.src
            title = item.find("div",{"class":"views-field-title"})
            title = title.h2.a.content
#views-field-field-website
# .a .urlind_all('a'):

        
    def setFields(self):
            set_fields_data(self.fields, self.new, self.data)
            
    def createItem(self):
        errors = Errors()
        new = self.new=self.form.factory()
        remoteURL = new.remoteURL
        try:
            result = web_preview(remoteURL, parser="html.parser")
            new.title = result[0]
            new.description = result[1]
            new.imageURL = result[2]
        except:

            error = Error("Failed to Fetch and Parse URL")
            errors.append(error)
        if hasattr(new,'imageURL'):
           self.setimage(new.imageURL) 
        return errors

        
#JUST TO MAKE IT EASIER TO UNDERSTAND        
class Edit(Update):
    pass
    
class SaveAndView(Update):
        def newURL(self,baseURL):
               return baseURL
           
class SaveAndViewHTML(Update):
        def newURL(self,baseURL):
               return baseURL + '/html'

class SaveAndViewJS(Update):
        def newURL(self,baseURL):
               return baseURL + '/javascript'

class SaveAndRoot(Update):
    def newURL(self,baseURL):
        return "/"

class SaveAndParent(Update):
    def newURL(self,baseURL):
        return ".."    

class SaveAndTest(Update):
        def newURL(self,baseURL):
               return self.form.context.testURL

class SaveAndViewURL(Update):
      def newURL(self,baseURL):
          return self.form.newURL(baseURL)
      
class Delete(Action):
    """Delete action for any locatable context.
    """
    successMessage = _(u"The object has been deleted.")
    failureMessage = _(u"This object could not be deleted.")

    def available(self, form):
        content = form.getContentData().getContent()
        if ILocation.providedBy(content):
            container = content.__parent__
            return (hasattr(container, '__delitem__') and
                    hasattr(container, '__contains__'))
        return False

    def __call__(self, form):
        content = form.getContentData().getContent()

        if ILocation.providedBy(content):
            container = content.__parent__
            name = content.__name__
            if name in container:
                try:
                    item = container[name]
                    root = getSiteRoot(item)
                    products = form.getProducts()
                    del container[name]
                    root.indexTree()
                    products.indexTree()
                    form.status = self.successMessage
                    form.message(form.status)
                    url = str(IURL(container, form.request))
                    url = url + '/manage'
                    return SuccessMarker('Deleted', True, url=url)
                except ValueError:
                    pass

        form.status = self.failureMessage
        form.message(form.status)
        return FAILURE
