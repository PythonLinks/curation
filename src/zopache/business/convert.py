from zopache.business.company import MapOrganization
from zopache.business.interfaces import IOrganization

def convert(item):
    new = MapOrganization()

    for attribute in [
                 'name',
                  'parent',
                 'address',
                 'title',
                 'description',
                 'focus',
                 'ballotStatus',
                 'remoteURL',
                 'source',
                 'duesURL',
                 'registerURL',
                 'joinURL',
                 'phone',
                 'twitterId',
                 'facebookId',
                 'facebookGroup',
                 'youTubeChannelURL',
                 'email',
                 'eventsPageURL',
                 'donationsPageURL']:
        setattr(new,attribute,getattr(item,attribute))

    for child in item.valuesAsList():
        childName = child.name
        del item[childName]
        new[childName] = child
        
    del item.parent[newName]
    parent[newName] = new

       
