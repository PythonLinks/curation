from zopache.pages.category import Category
from zopache.business.interfaces import IOrganization

class Convert(object):

  def convert(item):
    new = Category()
    parent = item.parent
    newName = item.name
    for attribute in [
                  'name',
                  'parent',
                  'title',
                  'description',
                  'source']:
        setattr(new,attribute,getattr(item,attribute))

    for child in item.allValuesAsList():
        childName = child.name
        del item[childName]
        new[childName] = child


    del item.parent[newName]
    parent[newName] = new


