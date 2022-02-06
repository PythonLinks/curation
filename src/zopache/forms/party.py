from dolmen.forms.base.markers import FAILURE, SUCCESS

from zopache.core.viewdecorators import *
from zopache.remote.rssarticle import IRSSArticle

from dolmen.forms.base import Actions

from zopache.ttw.interfaces import IInternalPrincipal
from zopache.crud.forms import EditForm
from zopache.ttw.treewidget import TreeField
from zopache.core.interfaces import ITreeSecurity
from zopache.crud.update import Cancel,Save

class IParty(Interface):
    category=TreeField(
           title="Category Search",
           description= """Choose where to move the articcle. """,
           required = False,
            )
    
class ChooseParty(Save):
    def __call__(self,form):
        result = Save.__call__(self,form)
        if result != FAILURE:
            self.publish()
            raise HTTPFound('/' + form.context.parent.name +'/manage')
        
        return result
    

        #    category = form.getSiteRoot()[context.category]
        #    if category!= context.__parent__:
        #        context.moveTo(category)


@form_component
@name ('party')
@context(IInternalPrincipal)
@implementer(ITreeSecurity)
class SelectParty (EditForm):
    title = 'Select your party.'
    subTitle = "So that we can connect you."
    interface = IParty
    def newURL (self,baseURL):
           return baseURL

    def addAuthorizedActions(self):
        self.actions = Actions(

                    ChooseYourParty("Choose Your Party","choose-party"),
                    Cancel("Cancel","Cancel"))
        
    def postProcess(self, view = None):
        self.siteRoot = self.getSiteRoot()
        context = self.context
        context.postProcess(view = self)
        
           


