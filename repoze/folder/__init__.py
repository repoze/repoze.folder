import sys

from zope.interface import implements

from zope.component.event import objectEventNotify

from persistent import Persistent

from repoze.folder.interfaces import IFolder
from repoze.folder.events import ObjectAddedEvent
from repoze.folder.events import ObjectWillBeAddedEvent
from repoze.folder.events import ObjectRemovedEvent
from repoze.folder.events import ObjectWillBeRemovedEvent

from BTrees.OOBTree import OOBTree
from BTrees.Length import Length

sysencoding = sys.getdefaultencoding()

class Folder(Persistent):
    """
    A folder implementation which acts much like a Python dictionary.
    The keys are Unicode strings; the values are arbitrary Python
    objects.
    """

    # _num_objects=None below is b/w compat for older instances of
    # folders which don't have a BTrees.Length object as a
    # _num_objects attribute.
    _num_objects = None 

    __name__ = None
    __parent__ = None

    implements(IFolder)

    def __init__(self, data=None):
        if data is None:
            data = {}
        self.data = OOBTree(data)
        self._num_objects = Length(len(data))

    def keys(self):
        """
        Returns an iterable object containing the names associated
        with the objects that appear in the folder.  Each name is
        guaranteed to be a Unicode string.
        """
        return self.data.keys()

    __iter__ = keys

    def __len__(self):
        """
        Returns the number of objects in the container.
        """
        if self._num_objects is None:
            # can be arbitrarily expensive
            return len(self.data)
        return self._num_objects()

    def __nonzero__(self):
        """ This is defined so code that does 'if folder:' will avoid
        calling __len__ (which can be arbitrarily expensive). """
        return True

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
        Each name is guaranteed to be a Unicode string.
        """
        return self.data.items()

    def __getitem__(self, name):
        """
        Return the named object, or raise ``KeyError`` if the object
        is not found.

        """
        name = unicodify(name)
        return self.data[name]

    def get(self, name, default=None):
        """
        Return the named object, or the value of the `default`
        argument if the object is not found.  Return the named object,
        or raise ``KeyError`` if the object is not found.

        `name`` will optimally be a Unicode string, because keys used
        to look up objects are stored as Unicode.  However, if
        ``name`` is a byte string, the system attempts to decode it to
        Unicode using the default system encoding; if it cannot be
        decoded using the system encoding, the system attempts to
        decode it using the UTF-8 codec; and if that fails, a
        TypeError is raised.
        """
        name = unicodify(name)
        return self.data.get(name, default)

    def __contains__(self, name):
        """
        Return true if the named object appears in the folder.

        `name`` will optimally be a Unicode string, because keys used
        to look up objects are stored as Unicode.  However, if
        ``name`` is a byte string, the system attempts to decode it to
        Unicode using the default system encoding; if it cannot be
        decoded using the system encoding, the system attempts to
        decode it using the UTF-8 codec; and if that fails, a
        TypeError is raised.
        """
        name = unicodify(name)
        return self.data.has_key(name)

    def __setitem__(self, name, other):
        """
        Add the given object to the folder under the given name.  The
        name must not be the empty string nor may it be of a type other
        than ``basestring`` (a TypeError is raised if either case is true).

        `name`` will optimally be a Unicode string, because keys used
        to look up objects are stored as Unicode.  However, if
        ``name`` is a byte string, the system attempts to decode it to
        Unicode using the default system encoding; if it cannot be
        decoded using the system encoding, the system attempts to
        decode it using the UTF-8 codec; and if that fails, a
        TypeError is raised.

        This method sends a ``ObjectWillBeAddedEvent`` before the
        object is set into the folder, and an ``ObjectAddedEvent``
        after the object has been set into the folder.
        """
        return self.add(name, other)

    def add(self, name, other, send_events=True):
        """ Does the same thing as ``__delitem__`` but provides the
        ``send_events`` argument to allow a user to suppress the
        sending of folder events.  By default, the ``send_events``
        flag is ``True``, meaning this method behaves exactly like
        ``__setitem__`` (events are sent).  If ``send_events`` is
        ``False`` or any other value that evaluates to false, folder
        events will not be sent.
        """
        if not isinstance(name, basestring):
            raise TypeError("Name must be a string rather than a %s" %
                            name.__class__.__name__)
        if not name:
            raise TypeError("Name must not be empty")

        name = unicodify(name)

        if self.data.has_key(name):
            raise KeyError('An object named %s already exists' % name)

        if send_events:
            objectEventNotify(ObjectWillBeAddedEvent(other, self, name))
        other.__parent__ = self
        other.__name__ = name

        # backwards compatibility: add a Length _num_objects to folders that
        # have none
        if self._num_objects is None:
            self._num_objects = Length(len(self.data))

        self.data[name] = other
        self._num_objects.change(1)
        if send_events:
            objectEventNotify(ObjectAddedEvent(other, self, name))

    def __delitem__(self, name):
        """
        Delete the named object from the folder. Raises a KeyError if
        the object is not found.

        `name`` will optimally be a Unicode string, because keys used
        to look up objects are stored as Unicode.  However, if
        ``name`` is a byte string, the system attempts to decode it to
        Unicode using the default system encoding; if it cannot be
        decoded using the system encoding, the system attempts to
        decode it using the UTF-8 codec; and if that fails, a
        TypeError is raised.

        This method sends a ``ObjectWillBeRemovedEvent`` before the
        object is set into the folder, and an ``ObjectRemovedEvent``
        after the object has been set into the folder.
        """
        return self.remove(name)

    def remove(self, name, send_events=True):
        """ Does the same thing as ``__delitem__`` but provides the
        ``send_events`` argument to allow a user to suppress the
        sending of folder events.  By default, the ``send_events``
        flag is ``True``, meaning this method behaves exactly like
        ``__delitem__`` (events are sent).  If ``send_events`` is
        ``False`` or any other value that evaluates to false, folder
        events will not be sent.
        """
        name = unicodify(name)
        other = self.data[name]

        if send_events:
            objectEventNotify(ObjectWillBeRemovedEvent(other, self, name))

        if hasattr(other, '__parent__'):
            del other.__parent__
        if hasattr(other, '__name__'):
            del other.__name__

        # backwards compatibility: add a Length _num_objects to folders that
        # have none
        if self._num_objects is None:
            self._num_objects = Length(len(self.data))

        del self.data[name]
        self._num_objects.change(-1)
        if send_events:
            objectEventNotify(ObjectRemovedEvent(other, self, name))

    def __repr__(self):
        klass = self.__class__
        classname = '%s.%s' % (klass.__module__, klass.__name__)
        return '<%s object %r at %#x>' % (classname,
                                          self.__name__,
                                          id(self))
    
def unicodify(name, encoding=None):
    if encoding is None:
        encoding = sysencoding
    try:
        name = unicode(name)
    except UnicodeError:
        if encoding in ('utf-8', 'utf8'):
            raise TypeError(
                'Byte string names be decodeable using the system encoding '
                'of "utf-8" (%s)' % name
                )
        try:
            name = unicode(name, 'utf-8')
        except UnicodeError:
            raise TypeError(
                'Byte string names be decodeable using either the system '
                'encoding of "%s" or the "utf-8" encoding (%s)' % (
                sysencoding, name)
                )

    return name

