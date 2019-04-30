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
    def postAddProcess(self):
        
        self.new.webApproved = False
    
@view_component
@name('addMap')
@title("Add Map")
@target(IView)
@permissions('AddContent')
@context(IMap)    
class AddMap(AddPageBase):
    subTitle = 'Add a map'
    interface = IMap
    label="Add a Map"
    factory = Map


    
