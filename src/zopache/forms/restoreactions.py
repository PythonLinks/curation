# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.
from cromlech.browser import IURL
from dolmen.forms.base import Action, SuccessMarker
from dolmen.forms.base.markers import FAILURE
from dolmen.forms.base.utils import set_fields_data, apply_data_event
from dolmen.message.utils import send
from cromlech.browser.exceptions import HTTPFound
from ZODB.ExportImport import ExportImport
from zopache.core.uniquename import UniqueName
from cromlech.browser.interfaces import IPublicationRoot

class BaseAction(Action):
    """Add action for files.
    """
    
    def __init__(self, title):
        super(Action, self).__init__(title)

    def __call__(self, form):
        self.form=form
        formData, errors = form.extractData()
        if errors:
            form.submissionError = errors
            return FAILURE
        
        branch=self.upload(formData)
        context = form.context
        self.processImport(context,branch)
        baseURL = self.form.contextURL()
        url = baseURL + "/manage"        
        return SuccessMarker('Added', True, url=url,code=307)


    def upload(self,formData):
        data  =  formData ['data']
        new = self.form.context._p_jar.importFile(data.file)
        return new


class RestoreAction(BaseAction):
    def processImport(self,context,branch):
        name = branch.__name__
        newName = UniqueName().uniqueName(context,name)          
        self.form.context [newName] = branch
        send(newName + " was restored")
        
class ReplaceAction(BaseAction):
    def processImport(self,context,branch):
        parent = context.__parent__
        nameInParent = context.__name__
        if IPublicationRoot.providedBy(context):
            nameInParent = "applicationRoot"
        del parent[nameInParent]
        parent[nameInParent] = branch
        branch.__name__ = nameInParent
        branch.__parent__ = parent
        self.form.context = branch
        send(nameInParent + " was replaced")        
        
        
