from zopache.core import Container
from zope.interface import implementer
from .interfaces import IProducts
from zopache.ttw.webclass import WebClass
from zopache.ttw.branch import Branch

@implementer(IProducts)
class Products(Branch,WebClass):
    icon="ttwicons/branch.svg"
    title = "Products"
    valuesByToken = {}
    def __init__(self):
        Container.__init__(self)


