# encoding: utf-8
# Copyright 2008 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
IPDA Site Project Management: unit tests for setup of the product.
'''

import unittest, doctest
from ipdasite.projectmgmt.tests.base import IPDAProjectMgmtTestCase
from Products.CMFCore.utils import getToolByName
from Testing import ZopeTestCase as ztc

class TestSetup(IPDAProjectMgmtTestCase):
    '''Test various aspects of setting up the IPDA Site Project Management.'''
    def testCatalogIndexes(self):
        '''Check if indexes are properly installed'''
        catalog = getToolByName(self.portal, 'portal_catalog')
        indexes = catalog.indexes()
        for i in ('active',):
            self.failUnless(i in indexes)
    def testCatalogMetadata(self):
        '''Check if indexed metadata (schema) are properly installed'''
        catalog = getToolByName(self.portal, 'portal_catalog')
        metadata = catalog.schema()
        for i in ('active',):
            self.failUnless(i in metadata)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
    
