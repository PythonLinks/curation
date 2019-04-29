from zopache.iodide.interfaces import IIodide
from zopache.pages.page import PageBase
from zopache.pages.cache import PageMixIn
from zopache.core.viewdecorators import *

@implementer (IIodide)     
class Iodide(PageBase, PageMixIn):
    webClass='Iodide'
    icon="ttwicons/Iodide.svg"

    
