Changes
=======

1.1 (2021-04-08)
----------------

- Add compatibility with latest zope.component versions

1.0 (2014-12-28)
----------------

- Add support for PyPy.

- Add support for Python 3.2, 3.3, and 3.4.

- Add support for testing on Travis.

- Drop support for Python 2.4 and 2.5.

0.6.3 (2012-03-29)
------------------

.. note::
   
   This release is the last which will maintain support for Python 2.4 /
   Python 2.5.

- Add support for continuous integration using ``tox`` and ``jenkins``.

- Add 'setup.py dev' alias (runs ``setup.py develop`` plus installs
  ``nose`` and ``coverage``).

- Move to GitHub.

0.6.2 (2010-10-04)
------------------

- Fix iteration bug due to use of ``_order`` as tuple.

0.6.1 (2010-10-01)
------------------

- Fixed persistence bugs in ordering support when adding or removing items.

0.6 (2010-09-30)
------------------

- Add support for ordering items in a folder.

0.5 (2010/09/04)
------------------

- Make ``remove`` return the removed object.

- Add ``pop`` method.

0.4 (2009/06/15)
------------------

- 100% test coverage.

- Add an ``add`` method that does what ``__setitem__`` does.  It also
  provides a flag named ``send_events``, which by default is True.  If
  it is False when ``add` is called, folder events
  (``IObjectWillBeAddedEvent`` and ``IObjectAddedEvent``) will not be
  sent.

- Add a ``remove`` method that does what ``__delitem__`` does.  It
  also provides a flag named ``send_events``, which by default is
  True.  If it is False when ``add` is called, folder events
  (``IObjectWillBeRemovedEvent`` and ``IObjectRemovedEvent``) will not
  be sent.

0.3.5 (2009/1/8)
------------------

- Add a ``BTrees.Length`` object to folders that don't already have
  one during ``__setitem__`` and ``__delitem__`` (this is an
  "evolution" step; having a Length object is useful for performance
  reasons).

0.3.4 (2009/1/8)
------------------

- Fix backwards compatibility foul (near
  ``self._num_objects.change(1)``: ``AttributeError: 'NoneType' object
  has no attribute 'change'``).

0.3.3 (2009/1/6)
------------------

- Add tests for ``unicodify`` and make docs about to-Unicode
  convenience conversion from byte strings (and error messages)
  slightly clearer.

- Now no matter what is passed to the folder as constructor, we
  try to turn it into an OOBTree (before it was set as ``data`` on the
  instance without any conversion).

- A ``__len__`` method was added to ``repoze.folder.Folder``
  instances.  It returns the number of subobjects in the folder.

- A ``_num_objects`` attribute is set onto newly created
  ``repoze.folder.Folder`` instances.  This is a
  ``BTrees.Length.Length`` object.  We manage this length object in
  order to supply a return value for the ``__len__`` method instead of
  using the folder's underlying OOBTree.__len__ method (querying a
  btree for length can be arbitrarily expensive).  A ``_num_objects``
  class attribute was added equalling None to provide a backward
  compatibility cue for already-persisted objects which do not have a
  meaningful Length attribute.

- The implementation no longer concerns itself with advertising a
  modified event (``IObjectModifiedEvent``).

0.3.2 (2008/12/13)
------------------

- Yeah.  0.3.1 was another brownbag, as we need to try to decode ASCII
  to unicode before we use the utf-8 decoding.

0.3.1 (2008/12/13)
------------------

- Mistakenly removed ``__parent__`` and ``__name__`` attributes from
  folder implementation, making 0.3 a brownbag.

0.3 (2008/12/13)
----------------

Backwards Incompatibilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- When a new object is added using ``__setitem__`` with the same name
  as an existing object, a KeyError is now raised rather than the item
  being silently replaced.

- API methods accepting a ``name`` (``__setitem__``, ``__getitem__``,
  ``get``, ``__contains__``, and ``__delitem__``) now attempt to
  decode bytestrings to Unicode using the utf-8 encoding before
  performing the action the method implies.

- Previously, it was possible to store either an ASCII bytestring or a
  Unicode object as a key value.  Now all key values are converted to
  Unicode before being stored.

0.2.1 (2008/10/31)
------------------

- Remove ``__init__`` from IFolder interface.
 
0.2 (2008/10/22)
------------------

- Update Sphinx docs, using interfaces

- Add folder ``__name__`` to repr and str of folder in output.

0.1 (2008/10/13)
------------------

- Initial release.
