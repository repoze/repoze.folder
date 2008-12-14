import unittest
from zope.component.testing import PlacelessSetup

class FolderTests(unittest.TestCase, PlacelessSetup):
    def setUp(self):
        PlacelessSetup.setUp(self)

    def tearDown(self):
        PlacelessSetup.tearDown(self)

    def _getTargetClass(self):
        from repoze.folder import Folder
        return Folder

    def _makeOne(self, data=None):
        klass = self._getTargetClass()
        return klass(data)

    def _registerEventListener(self, listener, iface):
        import zope.component
        gsm = zope.component.getGlobalSiteManager()
        from zope.interface import Interface
        gsm.registerHandler(listener, (Interface, iface,))

    def test_keys(self):
        folder = self._makeOne({'a':1, 'b':2})
        self.assertEqual(sorted(list(folder.keys())), ['a', 'b'])

    def test__iter__(self):
        folder = self._makeOne({'a':1, 'b':2})
        self.assertEqual(sorted(list(folder.__iter__())), ['a', 'b'])

    def test_values(self):
        folder = self._makeOne({'a':1, 'b':2})
        self.assertEqual(sorted(list(folder.values())), [1, 2])

    def test_items(self):
        folder = self._makeOne({'a':1, 'b':2})
        self.assertEqual(sorted(list(folder.items())), [('a', 1), ('b', 2)])

    def test___nonzero__(self):
        folder = self._makeOne()
        self.failUnless(folder)

    def test___setitem__nonstring(self):
        folder = self._makeOne()
        self.assertRaises(TypeError, folder.__setitem__, None)
        
    def test___setitem__8bitstring(self):
        folder = self._makeOne()
        self.assertRaises(TypeError, folder.__setitem__, '\xff')

    def test___setitem__empty(self):
        folder = self._makeOne()
        self.assertRaises(TypeError, folder.__setitem__, '')

    def test___setitem__(self):
        from repoze.folder.interfaces import IObjectEvent
        from repoze.folder.interfaces import IObjectWillBeAddedEvent
        from repoze.folder.interfaces import IObjectAddedEvent
        events = []
        def listener(object, event):
            events.append(event)
        self._registerEventListener(listener, IObjectEvent)
        dummy = DummyModel()
        folder = self._makeOne()
        folder['a'] = dummy
        self.assertEqual(len(events), 2)
        self.failUnless(IObjectWillBeAddedEvent.providedBy(events[0]))
        self.assertEqual(events[0].object, dummy)
        self.assertEqual(events[0].parent, folder)
        self.assertEqual(events[0].name, 'a')
        self.failUnless(IObjectAddedEvent.providedBy(events[1]))
        self.assertEqual(events[1].object, dummy)
        self.assertEqual(events[1].parent, folder)
        self.assertEqual(events[1].name, 'a')

    def test___setitem__exists(self):
        dummy = DummyModel()
        folder = self._makeOne({'a':dummy})
        self.assertRaises(KeyError, folder.__setitem__, 'a', dummy)

    def test___delitem__(self):
        from repoze.folder.interfaces import IObjectEvent
        from repoze.folder.interfaces import IObjectRemovedEvent
        from repoze.folder.interfaces import IObjectWillBeRemovedEvent
        events = []
        def listener(object, event):
            events.append(event)
        self._registerEventListener(listener, IObjectEvent)
        dummy = DummyModel()
        dummy.__parent__ = None
        dummy.__name__ = None
        folder = self._makeOne({'a':dummy})
        del folder['a']
        self.assertEqual(len(events), 2)
        self.failUnless(IObjectWillBeRemovedEvent.providedBy(events[0]))
        self.failUnless(IObjectRemovedEvent.providedBy(events[1]))
        self.assertEqual(events[0].object, dummy)
        self.assertEqual(events[0].parent, folder)
        self.assertEqual(events[0].name, 'a')
        self.assertEqual(events[1].object, dummy)
        self.assertEqual(events[1].parent, folder)
        self.assertEqual(events[1].name, 'a')
        self.failIf(hasattr(dummy, '__parent__'))
        self.failIf(hasattr(dummy, '__name__'))

    def test_repr(self):
        folder = self._makeOne()
        folder.__name__ = 'thefolder'
        r = repr(folder)
        self.failUnless(
            "<repoze.folder.Folder object 'thefolder' at " in r)
        self.failUnless(r.endswith('>'))

    def test_str(self):
        folder = self._makeOne()
        folder.__name__ = 'thefolder'
        r = str(folder)
        self.failUnless(
            "<repoze.folder.Folder object 'thefolder' at " in r)
        self.failUnless(r.endswith('>'))

    def test_unresolveable_unicode_setitem(self):
        name = unicode('La Pe\xc3\xb1a', 'utf-8').encode('latin-1')
        folder = self._makeOne()
        self.assertRaises(TypeError, folder.__setitem__, name, DummyModel())

    def test_resolveable_unicode_setitem(self):
        name = 'La Pe\xc3\xb1a'
        folder = self._makeOne()
        folder[name] = DummyModel()
        self.failUnless(folder.get(name))

    def test_unresolveable_unicode_getitem(self):
        name = unicode('La Pe\xc3\xb1a', 'utf-8').encode('latin-1')
        folder = self._makeOne()
        self.assertRaises(TypeError, folder.__getitem__, name)

    def test_resolveable_unicode_getitem(self):
        name = 'La Pe\xc3\xb1a'
        folder = self._makeOne()
        folder[name] = DummyModel()
        self.failUnless(folder[name])

class UnicodifyTests(unittest.TestCase):
    def _callFUT(self, name, encoding):
        from repoze.folder import unicodify
        return unicodify(name, encoding)

    def test_ascii_default_encoding_good(self):
        name = self._callFUT('abc', 'ascii')
        self.assertEqual(name, u'abc')

    def test_ascii_default_encoding_bad(self):
        name = unicode('La Pe\xc3\xb1a', 'utf-8').encode('utf-16')
        self.assertRaises(TypeError, self._callFUT, name, 'ascii')
        
    def test_utf_8_default_encoding_good(self):
        name = self._callFUT('abc', 'utf-8')
        self.assertEqual(name, u'abc')

    def test_utf_8_default_encoding_bad(self):
        name = unicode('La Pe\xc3\xb1a', 'utf-8').encode('utf-16')
        self.assertRaises(TypeError, self._callFUT, name, 'utf-8')

class DummyModel:
    pass

