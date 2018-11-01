from zope.interface import Interface
from zopache.crud.interfaces import IContainer
from dolmen.container import IBTreeContainer
from cromlech.container.interfaces import IOrdered

from zopache.ttw.interfaces import IUntrustedHTML

class IPage(IContainer,IOrdered ,IUntrustedHTML):
     pass

class INotPage (Interface):
     pass
