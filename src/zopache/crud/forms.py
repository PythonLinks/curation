# -*- coding: utf-8 -*-

#This software is subject to the CV and Zope Public Licenses.
from zope.interface import Interface
from dolmen.forms.base import DISPLAY
from zopache.crud import actions as formactions, i18n as _
from zopache.crud.utils import getFactoryFields, getAllFields
from cromlech.i18n import translate

from cromlech.security import getSecurityGuards, permissions

from .interfaces import IName, IContainer, ILeaf
from dolmen.container import BTreeContainer, IBTreeContainer
from zope.interface import implementer

from dolmen.forms.base import Actions
from dolmen.forms.base import Fields
from dolmen.forms.base import action, name, context, form_component

from .utilities import title_or_name    
from cromlech.webob import Response
from .interfaces import IEditable, IDeletable, IDisplayable
from zopache.core.baseform import Form

from cromlech.browser.directives import title


class AddForm(Form):
    """The add form itself is not protected. The security is checked on
    'update'. It checks if the 'require' directive of the factored item
    is respected on the context.
    """
    label= ''
    subTitle='Add an Object'

    @property
    def fields(self):
        return  Fields(IName,self.interface)

    @property
    def actions(self):
        return Actions(
            formactions.Add(_("Add","Add"), self.factory),
            formactions.Cancel(_("Cancel","Cancel")))

class AddByTitleForm(AddForm):
    @property
    def fields(self):
        return  Fields(self.interface)


    @property
    def actions(self):
        return Actions(
              formactions.AddByTitle("Add", self.factory),
              formactions.Cancel("Cancel"))    

class BaseEditForm(Form):    
    """
    """
    subTitle='Edit This Object'
    ignoreContent = False
    ignoreRequest = False
    actions = Actions(formactions.Edit(_("Save","Save")),
                    formactions.SaveAndView(_("SaveAndView","Save And View")),
                    formactions.Cancel(_("Cancel","Cancel")))
    @property
    def fields(self):
        if hasattr(self,'interface'):
            return  Fields(IName,self.interface).omit("__parent__")
        return Fields()

    @property
    def label(self):
        return ''
        #label = _(u"Edit this Object", default=u"Edit: $name",
        #          mapping={"name": title_or_name(self.context)})
        #return translate(label)

    @property
    def fields(self):
        edited = self.getContentData().getContent()
        return getAllFields(edited, '__parent__', '__name__')


    
class EditDemoForm(BaseEditForm):
    @property
    def actions(self):
        return Actions()
    
@form_component
@name (u'edit')
@context(IEditable)
@permissions('Manage')    
@title("Edit")
@permissions('Manage')
class EditForm(BaseEditForm):
    pass



@form_component
@name (u'display')
@context(IDisplayable)
@title("Display")
@title("Display")
@permissions('Manage')    
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
        #return title_or_name(self.context)

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
    actions = Actions(formactions.Delete(_("Delete","Delete")),
                      formactions.Cancel(_("Cancel","Cancel")))

    @property
    def label(self):
        return ''
        #label = u"Delete This Object?" 
        #return translate(label)


