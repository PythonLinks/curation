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

class BaseAction(Action,BaseBot):
    def successPage(self):
        form = self.form
        newURL = (Breadcrumbs.secureShortURL (form, form.getPrincipal())
                  + '/done')
        
        raise HTTPFound(newURL)
    
    def getAccessToken(self,form):
        self.form = form
        try:
           code = form.request.form['code']
           if len(code) == 0:
               raise Exception("Empty access token returned by Masotdon")
           mastodon= form.oauthProxy()
           userAccessToken = mastodon.log_in(code = code,
                                             redirect_uri= form.redirectURL(),
                                          scopes= form.SCOPES)
           return userAccessToken, SUCCESS
       
        except Exception as error:
            msg = "while trying to get the access code "
            msg +=  "was a problem. "
            msg += str(error)
            form.submissionError += msg
            return '', FAILURE

        
    def getUserInfo(self,form, userAccessToken):
        try:
            accountProxy = form.userProxy(userAccessToken)
            userAccount = accountProxy.me()
            return  userAccount, accountProxy, SUCCESS
        except Exception as error:
            msg = "while trying to get the User Info"
            msg +=  "was a problem. "
            msg += str(error)
            form.submissionError += msg
           
            return {},{}, FAILURE
        
    def updateAccount(self,accountProxy,userAccount,person):
                person.accountProxy = accountProxy
                person.userAccountDict = userAccount
                userAccount["mastodonDomain"] = self.form.context.mastodonDomain
    
class MastodonCallBackAction(BaseAction):
    def __call__(self, form):
        self.form = form
        
        userAccessToken, result = self.getAccessToken(form)

        if result == FAILURE:
            return FAILURE

        userAccount, accountProxy, result = self.getUserInfo(form,userAccessToken)

        if result == FAILURE:
            return FAILURE

        people = form.getPrincipalFolder()
        email = userAccount["username"] + '@' + form.context.mastodonDomain.lower()
                
        if email in people.idByEmail:
            personId = people.idByEmail[email]
            person = people [personId]
            self.updateAccount(accountProxy,userAccount,person)
            people.loginUser(person,form)
            self.successPage()
        else:
            values = {}
            values["form.field.userName"] = userAccount["username"] 
            values["form.field.displayName"] = userAccount["display_name"]
            values["form.field.mastodonDomain"] = form.context.mastodonDomain.lower()
            values["form.field.accessToken"] = userAccessToken
            values = form.urllibParseURLEncode(values)
            url = form.registerURL() + values
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

        self.updateAccount(accountProxy,userAccount,person)        
        
        people[newName]=new
        people.loginUser(person,form)
        new.name = newName
        siteRoot.addItem(new)
        #send("You are Registered")
        form.postAddProcess()
        self.successPage()

