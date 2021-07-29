from zopache.pages.page import Page
from zopache.business.interfaces import IOrganization

class Convert(object):
  newClass = Page
    
  def convert(item):
    new = Page()
    parent = item.parent
    for attribute in [
                  'name',
                  'parent',
                  'title',
                  'description',
                  'source']:
        setattr(new,attribute,getattr(item,attribute))

    for child in item.valuesAsList():
        childName = child.name
        del item[childName]
        new[childName] = child

    newName = item.name    
    del item.parent[newName]
    parent[newName] = new


