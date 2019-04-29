# Text line widget
from zope.interface import Interface
import crom
from dolmen.forms.base.interfaces import IWidget
from dolmen.forms.ztk.widgets import getTemplate
from dolmen.forms.ztk.fields import ( 
    SchemaField, SchemaFieldWidget, registerSchemaField)
from dolmen.forms.ztk.widgets.textline import  TextLineSchemaField
from zopache.ttw.interfaces import ITreeField
from zope.interface import Interface
from zope import schema
from zopache.pages.interfaces import IRootPage
import crom
from cromlech.browser.interfaces import IPublicationRoot

from zopache.crud.interfaces import IContainer
from zopache.zmi.interfaces import IURLSegment
from zopache.pages.interfaces import IPage, INotPage
from zopache.ttw.interfaces import IBranch
from zopache.ttw.interfaces import ITreeField 
from zope.interface import implementer  
from zope.interface import implementer
from zopache.core import getRoot

@implementer (ITreeField)
class  TreeField(schema.TextLine):
    pass



import crom
from dolmen.forms.base.interfaces import IField
@crom.adapter
@crom.sources(ITreeField)
@crom.target(IField)
class TreeSchemaField(SchemaField):
    """A Tree Field
    """

#def register():
registerSchemaField(TreeSchemaField, ITreeField)

@crom.adapter
@crom.target(IWidget)
@crom.sources(TreeSchemaField,Interface , Interface)
class TreeWidget(SchemaFieldWidget):
    defaultHtmlClass = ['field', 'field-textline']
    defaultHtmlAttributes = set(['readonly', 'required', 'autocomplete',
                                 'maxlength', 'pattern', 'placeholder',
                                 'size', 'style', 'disabled'])
    def update(self):
        root = getRoot(self.form.context)
        self.template = root['Products']['Templates']['fancytreewidget']
