from zope.interface import implements

from repoze.folder.interfaces import IObjectAddedEvent
from repoze.folder.interfaces import IObjectWillBeAddedEvent
from repoze.folder.interfaces import IObjectRemovedEvent
from repoze.folder.interfaces import IObjectWillBeRemovedEvent

class _ObjectEvent(object):
    def __init__(self, object, parent, name):
        self.object = object
        self.parent = parent
        self.name = name

class ObjectAddedEvent(_ObjectEvent):
    implements(IObjectAddedEvent)

class ObjectWillBeAddedEvent(_ObjectEvent):
    implements(IObjectWillBeAddedEvent)

class ObjectRemovedEvent(_ObjectEvent):
    implements(IObjectRemovedEvent)

class ObjectWillBeRemovedEvent(_ObjectEvent):
    implements(IObjectWillBeRemovedEvent)

class _ObjectOrderingEvent(object):
    def __init__(self, object, parent, name, previous_index, new_index):
        self.object = object
        self.parent = parent
        self.name = name
        self.previous_index = previous_index
        self.new_index = new_index
