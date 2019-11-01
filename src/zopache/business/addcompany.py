from dolmen.forms.base import Actions

from zopache.pages.pageactions import *
from zopache.crud import actions as formactions
from zopache.pages.pageactions import *
from zopache.core.viewdecorators import *
from zopache.ttw.html import CkScripts
from zopache.ttw.html import AddCkHTMLBase

from zopache.core.uniquename import UniqueName
from zopache.crud.forms import AddByTitleForm
from zopache.business.interfaces import IMap, ICompany, IOrganization
from zopache.business.company import Company, Organization
from zopache.business.map import Map
from zopache.pages.addpage import AddPageBase
from zopache.pages.interfaces import IPage


class AddBase(AddPageBase):
    count = 0 
    layoutName = "UserMenu"
    
    def postAddProcess(self):
        self.new.webApproved = False
        self.new.hidden = True        
        self.new.postAddProcess(self)
        
    @property
    def actions(self):
        return Actions(
              AddAndView("Add and View", self.factory),
              formactions.Cancel("Cancel","Cancel"))
    
    
@view_component
@name('addCompany')
@title("Add Company")
@target(IView)
@permissions('Vote')
@context(IMap)    
class AddCompany(AddBase):
    interface = ICompany
    label="Add a Company"
    factory = Company
    title = "Add a Company"
    subTitle = "All submissions are reviewed before being approved. "
    
@view_component
@name('addOrganization')
@title("Add Organization")
@target(IView)
@permissions('Vote')
@context(IMap)    
class AddOrganization(AddBase):
    interface = IOrganization
    factory = Organization
    title = "Add an Organization"
    subTitle = "All submissions are reviewed before being approved. "
    
        
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


    
