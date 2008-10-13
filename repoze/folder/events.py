from zope.interface import implements

from repoze.folder.interfaces import IObjectAddedEvent
from repoze.folder.interfaces import IObjectWillBeAddedEvent
from repoze.folder.interfaces import IObjectRemovedEvent
from repoze.folder.interfaces import IObjectWillBeRemovedEvent

class ObjectAddedEvent(object):
    implements(IObjectAddedEvent)
    def __init__(self, object, parent, name):
        self.object = object
        self.parent = parent
        self.name = name

class ObjectWillBeAddedEvent(object):
    implements(IObjectWillBeAddedEvent)
    def __init__(self, object, parent, name):
        self.object = object
        self.parent = parent
        self.name = name

class ObjectRemovedEvent(object):
    implements(IObjectRemovedEvent)
    def __init__(self, object, parent, name):
        self.object = object
        self.parent = parent
        self.name = name

class ObjectWillBeRemovedEvent(object):
    implements(IObjectWillBeRemovedEvent)
    def __init__(self, object, parent, name):
        self.object = object
        self.parent = parent
        self.name = name
    
