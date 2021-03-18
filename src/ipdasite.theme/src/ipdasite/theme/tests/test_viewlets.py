# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from ipdasite.theme.testing import IPDA_SITE_THEME_INTEGRATION_TESTING
from Products.Five.browser import BrowserView as View
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewlet, IViewletManager
import unittest2 as unittest

class ViewletTest(unittest.TestCase):
    layer = IPDA_SITE_THEME_INTEGRATION_TESTING
    def setUp(self):
        self.context = self.layer['portal']
        self.request = self.layer['app'].REQUEST
        self.view = View(self.context, self.request)
    def testViewletInterfaces(self):
        '''Ensure viewlet classes implement proper interfaces'''
        from ipdasite.theme.browser.agencies import AgenciesViewlet
        self.failUnless(IViewlet.implementedBy(AgenciesViewlet))

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
