repoze.folder
=============

``repoze.folder`` provides a barebones ZODB folder implementation with
object event support.  Folders have a dictionary-like interface and
emit "object events" on the addition and removal of objects when
certain methods of this interface are exercised.

Using a folder::

   >>> from repoze.folder import Folder
   >>> from persistent import Persistent
   >>> folder = Folder()
   >>> class Child(Persistent):
   >>>    pass
   >>> folder['child1'] = Child()
   >>> folder['child2'] = Child()
   >>> list(folder.keys())
   ['child1', 'child2']
   >>> folder.get('child1')
   <Child object at ELIDED>
   >>> del folder['child1']
   >>> list(folder.keys())
   ['child2']

Folder objects are based on BTree code, so as long as you persist
them, the folder should be able to contain many objects efficiently.
