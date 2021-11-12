# -*- coding: utf-8 -*-

#This software is subject to the CV and Zope Public Licenses.
from zope.interface import Interface
from dolmen.forms.base import DISPLAY

from zopache.core.viewdecorators import *

from dolmen.container import BTreeContainer, IBTreeContainer
from dolmen.forms.base import Actions

from .interfaces import IName, IContainer, ILeaf
from .interfaces import IEditable, IDeletable
from zopache.core.baseform import Form
from zopache.core.breadcrumbs import Breadcrumbs
from zopache.crud import actions as formactions, i18n as _
from zopache.crud import update as editactions
from zopache.crud.delete import DeleteAction
from zopache.crud.utils import getFactoryFields, getAllFields
from zopache.core.uniquename import UniqueName
from zopache.crud.actions import AddByName, AddByTitle
from zopache.ttw.mail import Notify

class AddFormBase(Form, Breadcrumbs):    
    """The add form itself is not protected. The security is checked on
    'update'. It checks if the 'require' directive of the factored item
    is respected on the context.
    """
    error = ''
    submissionError = ''
    label= ''
    subTitle='Add an Object'
    
    def acquireTitle(self):
         return self.title
     
    @property
    def fields(self):
        return  Fields(self.interface)

#USING TRADITIONAL PERMISSIONS    
class AddForm(AddFormBase):
    @property
    def fields(self):
        return  Fields(IName,self.interface)

    actions = Actions()
    #def actions(self):
    #    return  Actions(
    #        formactions.Add(_("Add","Add"), self.factory),
    #        formactions.Cancel(_("Cancel","Cancel")))
    
class TreeSecurityAddForm(AddFormBase):
    @property
    def fields(self):
        return  Fields(IName,self.interface)
    actions = Actions()
    
    def update(self):
        if self.treeSecurity():
           self.addAuthorizedActions()
        else:
           self.addUnauthorizedActions()
           
    def addAuthorizedActions(self):
        self.actions = Actions()
        
    def addUnAuthorizedActions():
        self.actions = Actions()        
   
    
#THIS ONE IS LIKE ADD FORM, BUT BASED ON TREE SECURITY    
class AddByNameForm(TreeSecurityAddForm,UniqueName):
    def addAuthorizedActions(self):
            self.actions = Actions(
            formactions.AddByName(_("Add","Add"), self.factory),
            formactions.Cancel(_("Cancel","Cancel")))
    
class AddByTitleForm(TreeSecurityAddForm,Notify):
    @property
    def fields(self):
        return  Fields(self.interface)
    
    def __init__(self,context,request):
        TreeSecurityAddForm.__init__(self,context,request) 
        Notify.__init__(self)       
    
    def addAuthorizedActions(self):   
              self.actions = Actions(
              formactions.AddByTitle("Add", self.factory),
              formactions.Cancel("Cancel"))

class BaseEditForm(Form,Breadcrumbs):    
    actions = Actions()
    subTitle='Edit This Object'
    ignoreContent = False
    ignoreRequest = False
    count = 0
    @property
    def fields(self):
        return  Fields(self.interface)
    
    def update(self):
        if self.treeSecurity():
            self.addAuthorizedActions()
        else:
            self.addUnAuthorizedActions()
            
    def addUnAuthorizedActions(self):
        self.actions = Actions()
        
    def addAuthorizedActions(self):

        self.actions = Actions(editactions.Edit(_("Save","Save")),
                    editactions.SaveAndView(_("SaveAndView","Save And View")),
                    editactions.Cancel(_("Cancel","Cancel")))

    @property
    def label(self):
        return ''

    @property
    def fields(self):
        edited = self.getContentData().getContent()
        return getAllFields(edited, '__parent__', '__name__')
    
class EditDemoForm(BaseEditForm):
    pass

class EditForm(BaseEditForm):
    pass


#@form_component
#@name (u'display')
#@context(IDisplayable)
#@title("Display")
#@title("Display")
#@permissions('Manage')


class DisplayForm(Form):
    """
    """
    label =''
    subTitle='Display This Object'
    mode = DISPLAY
    ignoreRequest = True
    ignoreContent = False

    @property
    def label(self):
        return ''

    @property
    def fields(self):
        displayed = self.getContentData().getContent()
        return getAllFields(displayed, '__parent__', '__name__', 'title')

@form_component
@name (u'delete')
@context(Interface)
@title("Delete")
@permissions('Manage')    
@title("Delete")
class DeleteForm(Form):
    """A confirmation for to delete an object.
    """
    label =''
    subTitle='Delete This Object'
    description = """Are you really sure ? This will also delete all of its 
children, and reindex the tree.<br><br> 
 If there are video objects (advanced version)
 in this branch of the tree, the links from the conference will not be 
deleted, and there will be trouble.  """
    actions = Actions(DeleteAction(_("Delete","Delete")),
                      formactions.Cancel(_("Cancel","Cancel")))

    @property
    def label(self):
        return ''
        #label = u"Delete This Object?" 
        #return translate(label)


