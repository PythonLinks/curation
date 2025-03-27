# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.

import sys
import random
import string
from dolmen.forms.base import Action, SuccessMarker
from dolmen.forms.base.markers import FAILURE
from dolmen.forms.base.utils import set_fields_data, apply_data_event
from cromlech.browser.exceptions import HTTPFound
from zopache.core.getroot import getPrincipalFolder, getSiteRoot

class RegisterAction(Action):

    def __call__(self, form):
        data, errors = form.extractData()
        if errors:
            form.submissionError = errors            
            form.submissionErrors = errors
            return FAILURE

        #SUCCESS, SO GO CREATE THE PERSON
        context = form.context
        newPerson= context.newPerson(form)
        form.new = newPerson

        #Subscribers only give en email address. 
        self.possiblyExtend(data)
        set_fields_data(form.fields, newPerson, data)
        
        #REGISTER AND LOG THE PERSON IN
        principalFolder = getPrincipalFolder (form.context,form)
        principalFolder [newName]=newPerson
        
        #You have to add it to the root index
        #before authenticating it.

        principalFolder.authenticate (data,form)
        #message(_(u"You are Registered and Logged In"))
        newURL = form.newURL(newPerson)
        newPerson.postAddProcess(view=form)    
        raise HTTPFound(newURL)
    
    def possiblyExtend(self,data):
        pass
    
class SubscribeAction(RegisterAction):
    def possiblyExtend(self,data):
        letters = string.ascii_letters + string.punctuation
        length = 20
        data["password"] = ''.join(random.choice(letters) for i in range(
            length))
        data["handle"] = data["email"]
