from dolmen.forms.base import Actions

from zopache.pages.pageactions import *
from zopache.crud import actions as formactions
from zopache.pages.pageactions import *
from zopache.core.viewdecorators import *
from zopache.ttw.html import CkScripts
from zopache.ttw.html import AddCkHTMLBase

from zopache.core.uniquename import UniqueName
from zopache.crud.forms import AddByTitleForm
from zopache.business.interfaces import IMap, ICompany
from zopache.business.company import Company
from zopache.business.map import Map
from zopache.pages.addpage import AddPageBase
from zopache.pages.interfaces import IPage


@view_component
@name('addCompany')
@title("Add Company")
@target(IView)
@permissions('Vote')
@context(IMap)    
class AddCompany(AddPageBase):
    interface = ICompany
    label="Add a Company"
    factory = Company
    
    @property
    def fields(self):
        fields = Fields(self.interface)
        if self.getHost() in ['rights.men','dev.pythonlinks.info']:
            fields = fields.omit('jobURL')        
        return  fields
    
    def postAddProcess(self):
        self.new.webApproved = False
        self.new.postAddProcess(self)
        
    @property
    def actions(self):
        return Actions(
              AddAndView("Add and View", self.factory),
              formactions.Cancel("Cancel","Cancel"))
    
        
@view_component
@name('addCompanyMap')
@title("Add Map")
@target(IView)
@permissions('AddContent')
@context(IPage)    
class AddMap(AddPageBase):
    subTitle = 'Add a map'
    interface = IMap
    label="Add a Map"
    factory = Map


    
