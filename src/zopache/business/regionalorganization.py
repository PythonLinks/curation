from BTrees.OOBTree import OOBTree
from zope.interface import implementer
from zopache.business.region import Region
from zopache.business.company import Organization
from zopache.business.interfaces import IRegionalOrganization

class RegionalOrganization(Organization,Region):
    webClass = 'SmallParty'
    zoom = 3.0
    def __init__(self):
       self.mapPoints =  OOBTree()
       Organization.__init__(self)
       Region.__init__(self)
