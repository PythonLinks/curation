Zopache.Crud
=============

Here we have forms for creating, updating, deleting (and soon) renaming basic
ZODB Objects.  

AddForm, DeleteForm, EditForm DisplayForm are what you should look for.

And then there are the interfaces.  If an object implements IAdding,
then subclasses of AddForm will work on it.  If an object implements
IDeleting, then the DeleteForm will work on those objects.  If an object
implements IDisplaying, then the display Form will work on it.  If an object
implements IEditing, then the Edit form will work on it. 

In practice you will want to subclass your interface off of IContainer, ILeaf, and
IRootContainer. Root containers cannot be deleted, and they cannot be renamed. 

To get all of this CRUD for free, what you have to do is define an interface object
for the class, and an add form.  You have to tell the class the interface it supports,
and you have to tell the add form the class to add (The factory variable), and the
context interfaces it can operate on. 

It is really very few lines of code to create new classes. 
Best to read the file models.py and views.py in the ZodbDemo. 