from BTrees.OOBTree import OOBTree
from zope.interface import implementer
from zopache.business.region import RegionBase
from zopache.business.company import Organization
from zopache.business.interfaces import IRegionalOrganization

class RegionalOrganization(Organization,RegionBase):
    webClass = 'SmallParty'
    zoom = 3.0
    def __init__(self):
       self.mapPoints =  OOBTree()
       Organization.__init__(self)
       Region.__init__(self)
