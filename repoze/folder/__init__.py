from zope.interface import implements

from zope.component.event import objectEventNotify

from persistent import Persistent

from repoze.folder.interfaces import IFolder
from repoze.folder.events import ObjectAddedEvent
from repoze.folder.events import ObjectWillBeAddedEvent
from repoze.folder.events import ObjectRemovedEvent
from repoze.folder.events import ObjectWillBeRemovedEvent

from BTrees.OOBTree import OOBTree

class Folder(Persistent):
    """The Folder implementation."""
    __parent__ = None
    __name__ = None

    implements(IFolder)

    def __init__(self, data=None):
        if data is None:
            self.data = OOBTree()
        else:
            self.data = data

    def keys(self):
        """Return a sequence-like object containing the names
           associated with the objects that appear in the folder
        """
        return self.data.keys()

    def __iter__(self):
        return iter(self.data.keys())

    def values(self):
        """Return a sequence-like object containing the objects that
           appear in the folder.
        """
        return self.data.values()

    def items(self):
        """Return a sequence-like object containing tuples of the form
           (name, object) for the objects that appear in the folder.
        """
        return self.data.items()

    def __getitem__(self, name):
        """Return the named object, or raise ``KeyError`` if the object
           is not found.
        """
        return self.data[name]

    def get(self, name, default=None):
        """Return the named object, or the value of the `default`
           argument if the object is not found.
        """
        return self.data.get(name, default)

    def __contains__(self, name):
        """Return true if the named object appears in the folder."""
        return self.data.has_key(name)

    def __nonzero__(self):
        return True

    def __setitem__(self, name, other):
        """Add the given object to the folder under the given name."""

        if not isinstance(name, basestring):
            raise TypeError("Name must be a string rather than a %s" %
                            name.__class__.__name__)
        try:
            unicode(name)
        except UnicodeError:
            raise TypeError("Non-unicode names must be 7-bit-ascii only")
        if not name:
            raise TypeError("Name must not be empty")

        if name in self.data:
            del self[name]

        objectEventNotify(ObjectWillBeAddedEvent(other, self, name))
        other.__parent__ = self
        other.__name__ = name
        self.data[name] = other
        objectEventNotify(ObjectAddedEvent(other, self, name))

    def __delitem__(self, name):
        """Delete the named object from the folder. Raises a KeyError
           if the object is not found."""
        other = self.data[name]
        objectEventNotify(ObjectWillBeRemovedEvent(other, self, name))
        if hasattr(other, '__parent__'):
            del other.__parent__
        if hasattr(other, '__name__'):
            del other.__name__
        del self.data[name]
        objectEventNotify(ObjectRemovedEvent(other, self, name))
        
