Using repoze.folder
===================

:mod:`repoze.folder` provides a barebones folder implementation with
object event support.  Folders have a dictionary-like interface and
emit "object events" on the addition and removal of objects when
certain methods of this interface are exercised.

Using a folder:

.. code-block:: python
   :linenos:

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

To subscribe to object events that occur when a folder's
``__setitem__`` or ``__delitem__`` is called, you can place ZCML in
your application's registry to handle the events::

  <subscriber for=".interfaces.IChild
                   repoze.folder.interfaces.IObjectAddedEvent"
              handler=".subscribers.child_added"/>

The event interface types are as follows::

  IObjectWillBeAddedEvent (before an object is seated into the folder)
  IObjectAddedEvent (after the object is seated into the folder)
  IObjectWillBeRemovedEvent (before the object is removed from the folder)
  IObjectRemovedEvent (after the object is removed from the folder)

See the ``repoze.folder.interfaces`` file for more information about
the folder API and the event object APIs.
