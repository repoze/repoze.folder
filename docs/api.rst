API Documentation for repoze.folder
======================================

Using a folder
--------------

.. code-block:: python
   :linenos:

   from repoze.folder import Folder
   f = Folder()

Folder interface
----------------

.. autointerface:: repoze.folder.interfaces.IFolder

Events sent when ``Folder.__setitem__`` called
----------------------------------------------

.. autointerface:: repoze.folder.interfaces.IObjectWillBeAddedEvent

.. autointerface:: repoze.folder.interfaces.IObjectAddedEvent

Events sent when ``Folder.__delitem__`` called
----------------------------------------------

.. autointerface:: repoze.folder.interfaces.IObjectWillBeRemovedEvent

.. autointerface:: repoze.folder.interfaces.IObjectRemovedEvent

