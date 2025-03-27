# -*- coding: utf-8 -*-

import sys

from mastodon import Mastodon

from cromlech.browser import IURL
from dolmen.forms.base import Action, SuccessMarker
from dolmen.forms.base.markers import FAILURE, SUCCESS
from dolmen.forms.base.utils import set_fields_data, apply_data_event
from cromlech.browser.exceptions import HTTPFound

from zopache.core.getroot import getPrincipalFolder
from zopache.pages.interfaces import IPage
from zopache.remote.mastodon.basebot import BaseBot
['write_media', 'write_statuses', 'read:accpimts']
from zopache.core.breadcrumbs import Breadcrumbs
from zopache.ttw.principalfolder import InternalPrincipal
class BaseAction(Action,BaseBot):
    def successPage(self):
        form = self.form
        newURL = (Breadcrumbs.secureShortURL (form, form.getPrincipal())
                  + '/done')        
        raise HTTPFound(newURL)
    
    def getUserProxy(self):
        form = self.form
        code = form.request.form['code']
        try:
           if len(code) == 0:
               raise Exception("Empty access token returned by Masotdon")       
        except Exception as error:
            msg = "while trying to get the access code "
            msg +=  "an empty access token was returned. "
            msg += str(error)
            form.submissionError += msg
            form.submissionErrors.append(msg)            
            return '', FAILURE
        
        try:
           mastodon = form.loginProxy(code)
           return mastodon, SUCCESS
        except Exception as error:
            msg = "while trying to get the access code "
            msg +=  "there was a problem. "
            msg += str(error)
            form.submissionError += msg
            form.submissionErrors.append(msg)
            return '', FAILURE

    def getUserInfo(self, userProxy):
        try:
            userInfo = userProxy.me()
            return  userInfo, SUCCESS
        except Exception as error:
            msg = "while trying to get the User Info"
            msg +=  "was a problem. "
            msg += str(error)
            self.form.submissionError += msg
            print (msg)
            return {},FAILURE
        
    
class MastodonCallBackAction(BaseAction):
    def __call__(self, form):
        self.form = form
        view = form
        userProxy, result = self.getUserProxy()
        if result == FAILURE:
            return FAILURE
        userAccount, result = self.getUserInfo(userProxy)
                                        
        if result == FAILURE:
            print ("\n\n")
            print ("FIRST FAILURE")            
            print ("\n\n")
            return FAILURE
        principalFolder = view.getPrincipalFolder()
        handle = userAccount["username"]         
        email = handle + '@' + form.context.mastodonDomainName()
        if email in principalFolder.idByEmail:
            personId = principalFolder.idByEmail[email]
            person = principalFolder [personId]
            person.updateAccount(userProxy,userAccount)
            principalFolder.loginUser(person,form)
            self.successPage()
        else:
            person = principalFolder.newPerson(self.form)
            self.form.new = person
            person.email = email
            person.handle = handle
            person.updateAccount(userProxy,userAccount)
            principalFolder [person.__name__] = person
            principalFolder.loginUser(person,form)            
            person.postAddProcess(view = form)
            url = form.secureShortURL(person)
            raise HTTPFound(url)

class MastodonRegisterAction(BaseAction):            
    def __call__(self,form):
        self.form = form

        #First do the usual validation
        data, errors = self.form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE

        #Now the custom stuff.
        userAccessToken = data['accessToken']
        userAccount, accountProxy, result = self.getUserInfo(form,userAccessToken)
        if result == FAILURE:
            return FAILURE

        new = form.factory()
        person = form.new=new
        people = form.getPrincipalFolder()
        siteRoot = form.getSiteRoot()        
        newName = siteRoot.getUniqueNumberString()
        new.name = newName
        person.updateAccount(accountProxy,userAccount)        
        people[newName]=new
        people.loginUser(person,form)
        new.name = newName
        siteRoot.addItem(new)
        #send("You are Registered")
        form.postAddProcess()
        self.successPage()

