from zope.component.interfaces import IObjectEvent
from zope.interface import Interface
from zope.interface import Attribute

class IObjectWillBeAddedEvent(IObjectEvent):
    """ An event type sent when an before an object is added """
    object = Attribute('The object being added')
    parent = Attribute('The folder to which the object is being added')
    name = Attribute('The name which the object is being added to the folder '
                     'with')

class IObjectAddedEvent(IObjectEvent):
    """ An event type sent when an object is added """
    object = Attribute('The object being added')
    parent = Attribute('The folder to which the object is being added')
    name = Attribute('The name which the object is being added to the folder '
                     'with')

class IObjectWillBeRemovedEvent(IObjectEvent):
    """ An event type sent before an object is removed """
    object = Attribute('The object being added')
    parent = Attribute('The folder to which the object is being added')
    name = Attribute('The name which the object is being added to the folder '
                     'with')

class IObjectRemovedEvent(IObjectEvent):
    """ An event type sent when an object is removed """
    object = Attribute('The object being added')
    parent = Attribute('The folder to which the object is being added')
    name = Attribute('The name which the object is being added to the folder '
                     'with')

class IFolder(Interface):
    """ A Folder implementation which stores objects using Unicode
    keys.  All methods which accept a ``name`` argument expect the
    name to either be Unicode or a byte string decodable using the
    default system encoding or the UTF-8 encoding."""
    def keys():
        """ Return a ``BTreeItems`` sequence representing the keys
        (object names) present in the folder.  Use list() against this
        value to expand eagerly."""
    def __iter__():
        """ An alias for ``keys`` """
    def values():
        """ Return a ``BTreeItems`` sequence representing the values
        (object values) present in the folder."""
    def items():
        """ Return a ``BTreeItems`` sequence representing the values
        (object values) present in the folder."""
    def get(name, default=None):
        """ Return the object value named by ``name`` or the default
        if the object name does not exist.  ``name`` must be a Unicode
        object or a bytestring object; if ``name`` is a bytestring
        object, it must be decodable using the system default encoding
        or the UTF-8 encoding."""
    def __contains__(name):
        """ Return ``True`` if the container contains the object value
        named by name, ``False`` otherwise. ``name`` must be a Unicode
        object or a bytestring object; if ``name`` is a bytestring
        object, it must be decodable using the system default encoding
        or the UTF-8 encoding."""
    def __nonzero__():
        """ Always return True """
    def __len__():
        """ Return the number of subobjects in this folder. """
    def __setitem__(name, other):
        """ Set an object into this folder using the name ``name`` and
        the value ``other``.  ``name`` must be a Unicode object or a
        bytestring object; if ``name`` is a bytestring object, it must
        be decodable using the system default encoding or the UTF-8
        encoding.  ``name`` cannot be the empty string.  When
        ``other`` is seated into this folder, it will also be
        decorated with a ``__parent__`` attribute (a reference to the
        folder into which it is being seated) and ``__name__``
        attribute (the name passed in to this function.  If a value
        already exists with the name ``name`` within this folder, a
        KeyError will be raised.  When this method is called, an
        ``ObjectWillBeAddedEvent`` event will be emitted before the
        object obtains a ``__name__`` or ``__parent__`` value.  After
        the object obtains a ``__name__`` and ``__parent__`` value, an
        ``ObjectAddedEvent`` will be emitted."""
    def add(name, other, send_events=True):
        """ Does the same thing as ``__delitem__`` but provides the
        ``send_events`` argument to allow a user to suppress the
        sending of folder events.  By default, the ``send_events``
        flag is ``True``, meaning this method behaves exactly like
        ``__setitem__`` (events are sent).  If ``send_events`` is
        ``False`` or any other value that evaluates to false, folder
        events will not be sent.
        """
    def __delitem__(name):
        """
        Delete an object value from this folder that is already
        present in the folder with the name ``name``.  ``name`` must
        be a Unicode object or a bytestring object; if ``name`` is a
        bytestring object, it must be decodable using the system
        default encoding or the UTF-8 encoding.  If the object value
        with the name ``name`` does not exist in the folder a
        ``KeyError`` will be raised.  When the object value referred
        to by ``name`` is deleted from this folder, its ``__parent__``
        and ``__name__`` values will be removed from the object.  When
        this method is called, an ``ObjectWillBeRemovedEvent`` event
        will be emitted before the object loses its ``__name__`` or
        ``__parent__`` values.  After the object loses its
        ``__name__`` and ``__parent__`` value, an
        ``ObjectRemovedEvent`` will be emitted.
        """
    def remove(name, send_events=True):
        """ Does the same thing as ``__delitem__`` but provides the
        ``send_events`` argument to allow a user to suppress the
        sending of folder events.  By default, the ``send_events``
        flag is ``True``, meaning this method behaves exactly like
        ``__delitem__`` (events are sent).  If ``send_events`` is
        ``False`` or any other value that evaluates to false, folder
        events will not be sent.
        """
