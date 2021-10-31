from zopache.core import Container
from zope.interface import implementer
from zopache.ttw.interfaces import IProducts, IWebClass
from zopache.ttw.webclass import WebClass
from zopache.ttw.branch import SimpleBranch

@implementer(IProducts)
class Products(SimpleBranch,WebClass):
    icon="ttwicons/branch.svg"
    title = "Products"
    def __init__(self):
        WebClass.__init__(self)
        SimpleBranch.__init__(self) #valuesByToken

    def indexBranch(self,tree,branch):
        for item in branch.values():
            if IWebClass.providedBy(item):
                self.indexBranch(tree,item)
                self.valuesByToken[item.__name__] = item
        

