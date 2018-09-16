# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.

import random
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
from zopache.core import getRoot
from dolmen.forms.base.utils import set_fields_data, apply_data_event

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

        data, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE
        obj= form.factory()
        form.new=obj
        root = getRoot(form.context)
        people = root ['person']
        anInteger = random.randint (1,sys.maxsize)
        while (True):
            anInteger += 1
            newName = str(anInteger)
            if not newName in people:
                break
        set_fields_data(form.fields, obj, data)            
        people[newName]=obj
        people.authenticate (data)
        message(_(u"You are Registered"))
        raise HTTPFound('/' + form.context.__name__)
    
