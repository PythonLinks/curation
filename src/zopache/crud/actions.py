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

from zopache.core.getroot import getSiteRoot
from zopache.crud import i18n as _
from zopache.core.uniquename import UniqueName
from zopache.core.transactionnote import TransactionNote
def message(message):
    send(message)


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


class Add(Action, UniqueName, TransactionNote):
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
        self.actuallyAdd(obj,data)
        obj.__parent__ = context
        message(_(u"Content created"))
        baseURL = self.form.url (obj)
        #baseURL = str(IURL(obj, form.request))
        self.describeWithView(obj,form)                
        if hasattr(form, 'newURL'):
           url=self.form.newURL(baseURL)
        else:
           url=self.newURL(baseURL)
        if hasattr(form,'postAddProcess'):
               form.postAddProcess()
        elif hasattr(form.new,'postAddProcess'):
               form.new.postAddProcess(view=form)

        return SuccessMarker('Added', True, url=url,code=307)

    def actuallyAdd(self,item,data):
        if hasattr(self.form, 'newName'):
           newName = self.form.newName(data)
        else:   
           newName = self.newName(data)
        self.form.context[newName]=item
        
    def newURL(self,baseURL):
        if hasattr(self.form, 'newURL'):
            return self.form.newURL(baseURL)
        else:
            return baseURL

    
    def newName(self,data):    
        name =  data['__name__']
        name = slugify(name, ok=SLUG_OK+'.', lower = False)
        context = self.form.context
        newName=self.uniqueContainerName(context,name,ofType="#")
        return newName

class AddNamed(Add):
    pass

class AddByTitle (Add):
    def actuallyAdd(self,item,data):
        newName = self.newName(data)
        self.form.context[newName]=item
        item.__name__ = newName
        root = getSiteRoot(self.form.context)
        if hasattr(root,'addItem'):
            root.addItem(self.new)
    
    def newName(self,data):    
        name =  data['title']
        name = slugify(name,lower=True)
        context = self.form.context
        
        #THERE COULD BE A LOCAL OBJECT WITH THE SAME NAME
        newName=self.uniqueContainerName(context,name,ofType="#")        
        newName=self.uniqueSiteName(context,name,ofType="-")
        return newName
    
    
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
        message(_(u"Content updated"))
        if hasattr(form,'postProcess'):        
               form.postProcess(view = form)
        elif hasattr(form.context,'postProcess'):
               form.context.postProcess(view=form)

        baseURL = str(IURL(form.context, form.request))
        url=self.newURL(baseURL)
        self.describeWithView(form.context,form)
        if url == form.request.url:
           return SuccessMarker('Updated', True)
        else:
           return SuccessMarker('Updated', True, url=url)

    def newURL(self,baseURL):
        if hasattr(self.form, 'newURL'):
            return self.form.newURL(baseURL)
        else:
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
                    message(form.status)
                    url = str(IURL(container, form.request))
                    url = url + '/manage'
                    return SuccessMarker('Deleted', True, url=url)
                except ValueError:
                    pass

        form.status = self.failureMessage
        message(form.status)
        return FAILURE
