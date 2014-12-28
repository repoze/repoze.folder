from zope.interface import implementer

from repoze.folder.interfaces import IObjectAddedEvent
from repoze.folder.interfaces import IObjectWillBeAddedEvent
from repoze.folder.interfaces import IObjectRemovedEvent
from repoze.folder.interfaces import IObjectWillBeRemovedEvent

class _ObjectEvent(object):
    def __init__(self, object, parent, name):
        self.object = object
        self.parent = parent
        self.name = name

@implementer(IObjectAddedEvent)
class ObjectAddedEvent(_ObjectEvent):
    pass

@implementer(IObjectWillBeAddedEvent)
class ObjectWillBeAddedEvent(_ObjectEvent):
    pass

@implementer(IObjectRemovedEvent)
class ObjectRemovedEvent(_ObjectEvent):
    pass

@implementer(IObjectWillBeRemovedEvent)
class ObjectWillBeRemovedEvent(_ObjectEvent):
    pass
