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
    """A Folder implementation.  The keys are Unicode strings, the
    values are arbitrary objects. """
    __name__ = None
    __parent__ = None

    implements(IFolder)

    def __init__(self, data=None):
        if data is None:
            self.data = OOBTree()
        else:
            self.data = data

    def keys(self):
        """
        Returns an iterable object containing the names associated
        with the objects that appear in the folder.
        """
        return self.data.keys()

    __iter__ = keys

    def values(self):
        """
        Return a sequence-like object containing the objects that
        appear in the folder.
        """
        return self.data.values()

    def items(self):
        """
        Return a sequence-like object containing tuples of the form
        (name, object) for the objects that appear in the folder.
        """
        return self.data.items()

    def __getitem__(self, name):
        """
        Return the named object, or raise ``KeyError`` if the object
        is not found.  If necessary, the name is decoded to Unicode
        using the UTF-8 encoding before the test is performed; if it
        cannot be decoded, a TypeError is raised.
        """
        name = unicodify(name)
        return self.data[name]

    def get(self, name, default=None):
        """
        Return the named object, or the value of the `default`
        argument if the object is not found.  Return the named object,
        or raise ``KeyError`` if the object is not found.  If
        necessary, the name is decoded to Unicode using the UTF-8
        encoding before it is used to look up the object; if it cannot
        be decoded, a TypeError is raised.
        """
        name = unicodify(name)
        return self.data.get(name, default)

    def __contains__(self, name):
        """
        Return true if the named object appears in the folder.  If
        necessary, the name is decoded to Unicode using the UTF-8
        encoding before it is used to perform the test; if it cannot
        be decoded, a TypeError is raised.
        """
        name = unicodify(name)
        return self.data.has_key(name)

    def __nonzero__(self):
        return True

    def __setitem__(self, name, other):
        """
        Add the given object to the folder under the given name.  The
        name must be a string or a unicode object and cannot be the
        empty string.  If necessary, the name is decoded to Unicode
        using the UTF-8 encoding before the object is stored; if it
        cannot be decoded, a TypeError is raised.
        """
        if not isinstance(name, basestring):
            raise TypeError("Name must be a string rather than a %s" %
                            name.__class__.__name__)
        if not name:
            raise TypeError("Name must not be empty")

        name = unicodify(name)

        if self.data.has_key(name):
            raise KeyError('An object named %s already exists' % name)

        objectEventNotify(ObjectWillBeAddedEvent(other, self, name))
        other.__parent__ = self
        other.__name__ = name
        self.data[name] = other
        objectEventNotify(ObjectAddedEvent(other, self, name))

    def __delitem__(self, name):
        """
        Delete the named object from the folder. Raises a KeyError if
        the object is not found. If necessary, the name is decoded to
        Unicode using the UTF-8 encoding before the object is deleted;
        if it cannot be decoded, a TypeError is raised.
        """
        name = unicodify(name)
        other = self.data[name]
        objectEventNotify(ObjectWillBeRemovedEvent(other, self, name))
        if hasattr(other, '__parent__'):
            del other.__parent__
        if hasattr(other, '__name__'):
            del other.__name__
        del self.data[name]
        objectEventNotify(ObjectRemovedEvent(other, self, name))

    def __repr__(self):
        klass = self.__class__
        classname = '%s.%s' % (klass.__module__, klass.__name__)
        return '<%s object %r at %#x>' % (classname,
                                          self.__name__,
                                          id(self))
    
def unicodify(name):
    try:
        name = unicode(name)
    except UnicodeError:
        try:
            name = unicode(name, 'utf-8')
        except UnicodeError:
            raise TypeError(
                "Non-unicode names must be decodeable using utf-8 (%s)" % name)
    return name

