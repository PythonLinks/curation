# -*- coding: utf-8 -*-

# Subject to ZPL and CV License agreements


from dolmen.container import BTreeContainer
from zope.interface import implementer
from .interfaces import IContent, IContentContainer
from .interfaces import IRootContentContainer
from zopache.crud.interfaces import  IContainer, ILeaf
from zopache.core import Leaf, Container, RootContainer
from zopache.ttw.html import TrustedHTML

#THIS IS BASICALLYT HE SAME THING AS A
#TTW CONTAINER, BUT THIS ONE IS FOR YOU TO
#CUSTOMIZE
@implementer(IContentContainer)
class ContentContainer(TrustedHTML,Container):
    title = "An HTML Container"
    source=u''
    webClass="Container"
    def __init__(self):
        Container.__init__(self)
        
@implementer(IRootContentContainer)
class TreeRoot(TrustedHTML,RootContainer):
    icon="ttwicons/Container.svg"
    title = "Zopache"
    source=''
    webClass="HomePage"    

    def __init__(self):
        RootContainer.__init__(self)            
        self.__name__= 'root'    


from zopache.core import Leaf    
#The IContent gives the object  attributes
@implementer(IContent) 
class Content(TrustedHTML,Leaf):
    webClass = "Content"
    icon="ttwicons/Note.svg"
    pass


