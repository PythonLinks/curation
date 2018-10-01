# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.

from cromlech.browser import IURL
from dolmen.forms.base import Action, SuccessMarker
from dolmen.forms.base.markers import FAILURE
from dolmen.forms.base.utils import set_fields_data, apply_data_event
from zopache.crud import i18n as _
from dolmen.message.utils import send
from cromlech.browser.exceptions import HTTPFound
from zope.event import notify
from zope.location import ILocation
from zope.lifecycleevent import ObjectCreatedEvent
from .utilities import uniqueName

def message(message):
    send(message)


class Cancel(Action):
    """Cancel the current form and return on the default content view.
    """

    def __call__(self, form):
        content = form.getContentData().getContent()
        url = str(IURL(content, form.request))
        return SuccessMarker('Aborted', True, url=url)


class Add(Action):
    """Add action for an IAdding context.
    """

    def __init__(self, title, factory):
        super(Add, self).__init__(title)
        self.factory = factory

    def __call__(self, form):
        self.form=form
        data, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE
        obj= form.factory()
        form.new=obj
        context=form.context
        set_fields_data(form.fields, obj, data)
        notify(ObjectCreatedEvent(obj))
        name=data['__name__']
        newName=uniqueName(context,name,ofType="#")
        context[newName]=obj
        message(_(u"Content created"))
        baseURL = str(IURL(obj, form.request))    
        self.new=form.new=obj
        url=self.newURL(baseURL)
        form.new.postProcess()
        form.postAddProcess()        
        return SuccessMarker('Added', True, url=url,code=307)

    def newURL(self,baseURL):
        return baseURL

class AddAndView(Add):
    def newURL(self,baseURL):
        return baseURL + '/index'        
    
class Update(Action):
    """Update action for any locatable object.
    """

    def __call__(self, form):
        import pdb; pdb.set_trace()
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
                    del container[name]
                    form.status = self.successMessage
                    message(form.status)
                    url = str(IURL(container, form.request))
                    return SuccessMarker('Deleted', True, url=url)
                except ValueError:
                    pass

        form.status = self.failureMessage
        message(form.status)
        return FAILURE
