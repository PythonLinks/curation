# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.
from slugify import slugify, SLUG_OK
from zope.event import notify
from zope.location import ILocation
from zope.lifecycleevent import ObjectCreatedEvent

from cromlech.browser import IURL
from dolmen.forms.base import Action, SuccessMarker
from dolmen.forms.base.markers import FAILURE
from dolmen.forms.base.utils import set_fields_data, apply_data_event
from dolmen.message.utils import send
from cromlech.browser.exceptions import HTTPFound

from zopache.core import getRoot
from zopache.crud import i18n as _
from zopache.core.uniquename import UniqueName

def message(message):
    send(message)


class Cancel(Action):
    """Cancel the current form and return on the default content view.
    """

    def __call__(self, form):
        content = form.getContentData().getContent()
        url = str(IURL(content, form.request))
        return SuccessMarker('Aborted', True, url=url)


class Add(Action, UniqueName):
    """Add action for an IAdding context.
    """

    def __init__(self, title, factory):
        Action.__init__(self,title)
        self.factory = factory

    def __call__(self, form):
        self.form=form
        data, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE
        obj= form.factory()
        self.new=form.new=obj
        context=form.context
        set_fields_data(form.fields, obj, data)
        notify(ObjectCreatedEvent(obj))
        newName = self.newName(data)
        newName = slugify(newName, ok=SLUG_OK+'.', lower = False)
        context[newName]=obj
        message(_(u"Content created"))
        baseURL = str(IURL(obj, form.request))    
        url=self.newURL(baseURL)
        form.new.postProcess()
        if hasattr(form.new,'postAddProcess'):
            try: 
               form.new.postAddProcess(view=form)
            except:
               form.new.postAddProcess()                
        form.postAddProcess()                
        return SuccessMarker('Added', True, url=url,code=307)

    def newName(self,data):    
        name =  data['__name__']
        name = slugify(name, lower = False)
        context = self.form.context
        newName=self.uniqueName(context,name,ofType="#")
        return newName
    
    def newURL(self,baseURL):
        return baseURL

class AddByTitle (Add):
    def newName(self,data):    
        name =  data['title']
        name = slugify(name,lower=True)
        context = self.form.context
        newName=self.uniqueName(context,name,ofType="-")
        return newName
    
    
class AddAndView(Add):
    def newURL(self,baseURL):
        return baseURL + '/index'        
    
class Update(Action):
    """Update action for any locatable object.
    """

    def __call__(self, form):
        self.form=form
        data, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE

        apply_data_event(form.fields, form.getContentData(), data)
        message(_(u"Content updated"))
        form.postProcess()
        baseURL = str(IURL(form.context, form.request))
        url=self.newURL(baseURL)
        if url == form.request.url:
           return SuccessMarker('Updated', True)
        else:
           return SuccessMarker('Updated', True, url=url)

    def newURL(self,baseURL):
            return self.form.request.url

    def postProcess(self):
            pass
        
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
                    root = getRoot(item)
                    del container[name]
                    root.indexTree()
                    root.indexTree()
                    root['Products'].indexTree()                    
                    form.status = self.successMessage
                    message(form.status)
                    url = str(IURL(container, form.request))
                    url = url + '/manage'
                    return SuccessMarker('Deleted', True, url=url)
                except ValueError:
                    pass

        form.status = self.failureMessage
        message(form.status)
        return FAILURE
