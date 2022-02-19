from zopache.crud.addbytitleactions import *
from zopache.core.viewdecorators import *

from zopache.crud.forms import AddByTitleForm
from zopache.pages.interfaces import IPage,IPageBase
from zopache.business.exists import Duplicate
from zopache.json.interfaces import  IAddNewsLetter
from zopache.json.newsletter import  NewsLetter
from zopache.core.interfaces import ITreeSecurity


#ADD NEWS
@view_component
@name('addNews')
@target(IView)
@context(IPageBase)
class AddNewsLetter(AddByTitleForm):
    interface = IAddNewsLetter
    emailApparoved = True
    title = "Add a News Letter"
    subtitle = "Because the MSM does not cover it."
    factory = NewsLetter

