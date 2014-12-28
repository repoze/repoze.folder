repoze.folder
=============

.. image:: https://travis-ci.org/repoze/repoze.folder.png?branch=master
        :target: https://travis-ci.org/repoze/repoze.folder

.. image:: https://readthedocs.org/projects/repozefolder/badge/?version=latest
        :target: http://repozefolder.readthedocs.org/en/latest/
        :alt: Documentation Status

``repoze.folder`` provides a barebones ZODB folder implementation with
object event support.  Folders have a dictionary-like interface and
emit "object events" on the addition and removal of objects when
certain methods of this interface are exercised.

Folder objects are based on BTree code, so as long as you persist
them, the folder should be able to contain many objects efficiently.
