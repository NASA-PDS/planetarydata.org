# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from Products.Archetypes.tests.utils import makeContent
from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
from ipdasite.services.testing import IPDA_SITE_SERVICES_INTEGRATION_TESTING
from plone.app.testing import setRoles, TEST_USER_ID
import unittest

class WidgetsTest(unittest.TestCase):
    def testWidgetSizes(self):
        from ipdasite.services.content.registryobject import RegistryObjectSchema
        self.assertEquals(50, RegistryObjectSchema['lid'].widget.size)
        from ipdasite.services.content.identifiable import IdentifiableSchema
        self.assertEquals(50, IdentifiableSchema['guid'].widget.size)
        from ipdasite.services.content.servicebinding import ServiceBindingSchema
        self.assertEquals(50, ServiceBindingSchema['accessURI'].widget.size)
    def testWidgetTypes(self):
        from ipdasite.services.content.specificationlink import SpecificationLinkSchema
        from archetypes.referencebrowserwidget import ReferenceBrowserWidget
        self.failUnless(ReferenceBrowserWidget is SpecificationLinkSchema['specificationObject'].widget.__class__)
        self.assertEquals('/', SpecificationLinkSchema['specificationObject'].widget.startup_directory)
        from Products.Archetypes.atapi import TextAreaWidget
        self.failUnless(TextAreaWidget is SpecificationLinkSchema['usageDescription'].widget.__class__)

class TypesTest(unittest.TestCase):
    layer = IPDA_SITE_SERVICES_INTEGRATION_TESTING
    def setUp(self):
        super(TypesTest, self).setUp()
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        makeContent(self.portal, portal_type='Service Registry', id='registry-1')
        self.registry = self.portal['registry-1']
        makeContent(self.registry, portal_type='Service', id='service-1')
        self.service = self.registry['service-1']
    def tearDown(self):
        self.registry.manage_delObjects(self.service.id)
        self.portal.manage_delObjects(self.registry.id)
        super(TypesTest, self).tearDown()
    def testIfGUIDsAreURNs(self):
        self.assertEquals(u'urn:uuid:', self.service.guid[0:9])

class SetupTest(unittest.TestCase):
    '''Other setup-related tests not otherwise more specific.'''
    layer = IPDA_SITE_SERVICES_INTEGRATION_TESTING
    def setUp(self):
        super(SetupTest, self).setUp()
        self.portal = self.layer['portal']
    def testCatalogIndexes(self):
        '''Ensure package-specific indexes are installed'''
        indexes = getToolByName(self.portal, 'portal_catalog').indexes()
        for i in ('versionID', 'lid'):
            self.failUnless(i in indexes, 'Index "%s" missing in catalog' % i)
    def testCatalogMetadata(self):
        '''Check if indexed metadata schema are properly installed'''
        schema = getToolByName(self.portal, 'portal_catalog').schema()
        for i in ('versionID',):
            self.failUnless(i in schema, 'Metadata column "%s" missing in catalog schema' % i)


class VocabularyTest(unittest.TestCase):
    '''Ensure our vocabularies are present and contain expected values'''
    layer = IPDA_SITE_SERVICES_INTEGRATION_TESTING
    def setUp(self):
        super(VocabularyTest, self).setUp()
        self.portal = self.layer['portal']
    def testServiceCategoriesVocabulary(self):
        categoryVocabFactory = queryUtility(IVocabularyFactory, name=u'ipdasite.services.ServiceCategories')
        self.failIf(categoryVocabFactory is None)
        vocabulary = categoryVocabFactory(self.portal)
        self.assertEquals(9, len(vocabulary))
        for t in (
            u'Planning', u'Design', u'Generation', u'Validation', u'Search/retrieve', u'Data reader', u'Analysis',
            u'Dissemination', u'Visualization'
        ):
            self.failUnless(t in vocabulary, u'Vocabulary term "%s" missing from ipdasite.services.ServiceCategories' % t)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
