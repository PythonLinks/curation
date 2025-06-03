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

class MastodonCallBackAction(Action,BaseBot):
    def __call__(self, form):
        self.form = form
        view = form
        userProxy, result = self.getUserProxy()
        if result == FAILURE:
            return FAILURE
        userAccount, result = self.getUserInfo(userProxy)
                                        
        if result == FAILURE:
            return FAILURE
        
        principalFolder = view.getPrincipalFolder()
        userName = userAccount["username"]         
        email = userName + '@' + form.context.mastodonDomainName()
        handle = "@" + email
        if email in principalFolder.idByEmail:
            personId = principalFolder.idByEmail[email]
            person = principalFolder [personId]
            person.updateAccount(userProxy,userAccount)
            principalFolder.loginUser(person,form)
            self.nextPage()
        else:
            person = principalFolder.newPerson(self.form)
            self.form.new = person
            person.email = email
            person.handle = handle
            person.updateAccount(userProxy,userAccount)
            principalFolder [person.__name__] = person
            principalFolder.loginUser(person,form)            
            person.postAddProcess(view = form)
            self.goToGDPR()            

    def nextPage(self):
       principal = self.form.request.principal
       if ( principal.chatPermission and
            principal.postalCode):
            self.goHome()
       else:
            self.goToGDPR()
    
    def goToGDPR(self):
        form = self.form
        newURL = (self.form.getSecureLongURL (
                   context = form.getPrincipal())
                  + '/gdpr')        
        raise HTTPFound(newURL)

    def goHome(self):
        form = self.form
        newURL = self.form.getSiteRoot().homePage
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
        
    
