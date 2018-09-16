from zopache.core import Container
from zope.interface import implementer
from .interfaces import IProducts


@implementer(IProducts)
class Products(Container):
    icon="ttwicons/Container.svg"
    title = "Products"
    def __init__(self):
        Container.__init__(self)


