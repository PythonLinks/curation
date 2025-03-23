from zope import schema

from zope.interface import Interface
from cromlech.security import permissions
from dolmen.forms.base import Fields 
from dolmen.forms.base import Actions

from zopache.core.viewdecorators import *
from zopache.core.baseform import Form
from zopache.json.interfaces import IMultilingual,IMultilingualLeaf
from zopache.forms.translateactions import (OneLanguage,
                                            OneNode,
                                            languages
                                            )
from zopache.crud.actions import Cancel

class ITranslate(Interface):
      targetLanguage= schema.TextLine(
        title='Enter the 2 letter target language code',
          description = "Legal languages are de, es, fr, pl, tr and ja.",
            required=False)

@form_component
@context(IMultilingual)
@target(IView)
@name("translate")
@permissions('Manage')
class Translate(Form):
    title = "Translate"
    fields = Fields(ITranslate)
    subTitle = "This node to all languages, or all nodes to one language."

    @property
    def actions(self):
        return Actions(
              OneLanguage("Translate Branch"),
              OneNode("Translate Node"),              
              Cancel("Cancel","Cancel"))

@form_component
@context(IMultilingualLeaf)
@target(IView)
@name("translate")
@permissions('Manage')
class TranslateLeaf(Form):
    title = "Translate"
    subTitle = "The title and content."

    @property
    def actions(self):
        return Actions(
              OneNode("Translate Node"),              
              Cancel("Cancel","Cancel"))
