
from zopache.business.region import Region
from zopache.pages.category import Category
from zopache.business.interfaces import IRegionalCategory


@implementer(IRegionalCategory)
class RegionalCategory(Category,Region):
    webClass = "RegionalCategory"
    def __init__(self):
        Region.__init__(self)
        Category.__init__(self)

        
        
    


