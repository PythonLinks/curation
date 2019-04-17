# -*- coding: utf-8 -*-
#This software is subject to the CV and Zope Public Licenses.

from cromlech.webob.response import Response
import dolmen
from dolmen.template import TALTemplate
from dolmen.view import View, make_layout_response
from dolmen.forms.base import Form as BaseForm
from cromlech.location import get_absolute_url

from . import tal_template

from .scripts import Scripts

from dolmen.container import IBTreeContainer
from .breadcrumbs import Breadcrumbs

#FOR MONKEY PATCHING ACTION WIDGETS
def htmlClass(self):
    return "action btn"

class Form(BaseForm,Scripts,Breadcrumbs):
    title=""
    subTitle=u""
    responseFactory = Response
    make_response = make_layout_response
    template = tal_template('form.pt')

    @property
    def action_url(self):
        return self.request.url
            
    def widgetDictionary(self):
        return {c.htmlId():c for c in self.bootstrapWidgets()}

    def fieldDictionary(self):
        return {c.__name__:c for c in self.fields}    

    def isBool(self,widget):
        return widget.component._field._type==type(True)

    def isCheckBoxList (self,widget):
        return  widget.__class__.__name__=='MultiChoiceFieldWidget'

    def bootstrap_widgets(self):
        return self.bootstrapWidgets()
    
    def bootstrapWidgets(self):
        """Adds the needed css classes for bootstrap styles.
        """
        for widget in self.fieldWidgets:
            pass
        result = []
        for widget in self.fieldWidgets:
            defaultHtmlClass = widget.defaultHtmlClass
            if  self.isBool(widget) or self.isCheckBoxList(widget):
               if not 'form-check-input' in defaultHtmlClass: 
                   widget.defaultHtmlClass.append('form-check-input')
            else:
                if not ('form-control' in defaultHtmlClass):                 
                   widget.defaultHtmlClass.append('form-control')
            result.append (widget)
        return result

    def bootstrapActionWidgets(self):
           """Adds the needed css classes for bootstrap styles.
           """
           dolmen.forms.base.widgets.ActionWidget.htmlClass = htmlClass
           result = []
           for widget in self.actionWidgets:
               result.append (widget)
           return result

    def isBTreeContainer(self):
         return  IBTreeContainer.providedBy(self.context)

    #USED BY HTML TO COMPILE THE TEMPLATE
    def postProcess(self):
         pass

    def postAddProcess(self):
         pass     

    def breadcrumbs(self):
        return self.breadcrumbsManage()


