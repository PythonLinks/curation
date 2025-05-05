from zopache.business.company import MapOrganization
from zopache.json.jsonmaporganization import JSONMapOrganization

def bases(aClass,indent):
    for item in aClass.__bases__:
        print (indent * '-', item.__name__)
        bases(item,indent + 2)

def test():        
    print ('JSONMapOrganization')        
    bases(RegionalOrganization,2)
    print()
    print()
    print('MapOrganization')          
    bases(MapOrganization,2)
