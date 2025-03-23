from zopache.business.company import MapOrganization
from zopache.business.regionalorganization import RegionalOrganization

def bases(aClass,indent):
    for item in aClass.__bases__:
        print (indent * '-', item.__name__)
        bases(item,indent + 2)

def test():        
    print ('RegionalOrganization')        
    bases(RegionalOrganization,2)
    print()
    print()
    print('MapOrganization')          
    bases(MapOrganization,2)
