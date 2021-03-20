from zopache.business.company import MapOrganization
from zopache.business.interfaces import IOrganization

def convert(item):
    new = MapOrganization()
    parent = item.parent
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
                 'phone',
                 'twitterId',
                 'facebookId',
                 'facebookGroup',
                 'donationsPageURL',
                 'youTubeChanneURL',            
                 'email',
                 'eventsPageURL',
                 'donationsPageURL']:
        setattr(new,attribute,getattr(item,attribute))

    for child in item.valuesAsList():
        childName = child.name
        del item[childName]
        new[childName] = child

    newName = item.name    
    del item.parent[newName]
    parent[newName] = new

       
