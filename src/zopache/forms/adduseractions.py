# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.

import sys
from cromlech.browser import IURL
from dolmen.forms.base import Action, SuccessMarker
from dolmen.forms.base.markers import FAILURE
from dolmen.forms.base.utils import set_fields_data, apply_data_event
from zopache.crud import i18n as _
from cromlech.browser.exceptions import HTTPFound
from zope.event import notify
from zope.location import ILocation
from zope.lifecycleevent import ObjectCreatedEvent

from dolmen.forms.base.utils import set_fields_data, apply_data_event

from zopache.core.getroot import getPrincipalFolder, getSiteRoot
from zopache.pages.interfaces import INotPage
from zopache.crud.actions import Cancel

class Add(Action):

    def __call__(self, form):
        data, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE

        #SUCCESS, SO GO CREATE THE PERSON
        context = form.context
        newPerson= form.factory()
        newPerson.__parent__ = context
        root = getSiteRoot(context,form)
        newName = root.getUniqueNumberString()
        newPerson.__name__= newName
        root.addItem(newPerson)
        #You have to set the name before setting the email.
        #Because it updates the email->name index.
        set_fields_data(form.fields, newPerson, data)
        
        #REGISTER AND LOG THE PERSON IN
        principalFolder = getPrincipalFolder (form.context,form)
        principalFolder [newName]=newPerson
        #You have to add it to the root index
        #before authenticating it.
        principalFolder.authenticate (data,form)
        #message(_(u"You are Registered and Logged In"))
        newURL = form.newURL(newPerson)
        form.new=newPerson
        newPerson.postAddProcess(view=form)    
        raise HTTPFound(newURL)

    
