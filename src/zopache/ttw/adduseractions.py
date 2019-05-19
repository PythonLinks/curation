# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.

import sys
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
from zopache.core import getPrincipalFolder, getRoot
from dolmen.forms.base.utils import set_fields_data, apply_data_event
from zopache.pages.interfaces import INotPage

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

    def __init__(self, title, view):
        super(Add, self).__init__(title)
        self.factory = view.factory
        self.view = view

    def __call__(self, form):
        data, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE

        #SUCCESS, SO GO CREATE THE PERSON
        context = form.context
        newPerson= form.factory()
        newPerson.__parent__ = context
        root = getRoot(context)
        newName = root.getUniqueNumberString()
        newPerson.__name__= newName
        root.addItem(newPerson)
        #You have to set the name before setting the email.
        #Because it updates the email->name index.
        set_fields_data(form.fields, newPerson, data)
        
        #REGISTER AND LOG THE PERSON IN
        principalFolder = getPrincipalFolder (form.context)
        principalFolder [newName]=newPerson
        #You have to add it to the root index
        #before authenticating it.
        principalFolder.authenticate (data)
        message(_(u"You are Registered and Logged In"))
        newURL = form.newURL(newPerson)
        if hasattr(form,'postAddProcess'):
              form.new=newPerson            
              form.postAddProcess()    
        raise HTTPFound(newURL)

    
        """
        CODE I MIGHT NEED IN THE FUTURE
        newPerson.__parent__ = context
        self.form = form


        if INotPage.providedBy(self.form.context):
            newURL = self.form.url(newPerson) + '/speakerregistration'
        else:
        """



        
