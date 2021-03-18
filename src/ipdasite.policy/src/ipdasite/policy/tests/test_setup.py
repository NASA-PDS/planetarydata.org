# encoding: utf-8
# Copyright 2008-2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''IPDA Site Policy: unit tests for site setup.
'''

import unittest
from ipdasite.policy.testing import IPDA_SITE_POLICY_INTEGRATION_TESTING
from Products.CMFCore.utils import getToolByName


class SetupTest(unittest.TestCase):
    '''Unit tests the setup of the IPDA site policy.'''
    layer = IPDA_SITE_POLICY_INTEGRATION_TESTING
    def setUp(self):
        super(SetupTest, self).setUp()
        self.portal = self.layer['portal']
    def testPortalTitle(self):
        self.assertEquals(u'IPDA', self.portal.getProperty('title'))
    def testPortalDescription(self):
        self.assertEquals(u'International Planetary Data Alliance', self.portal.getProperty('description'))
    def testCSSAttribution(self):
        actions = getToolByName(self.portal, 'portal_actions')
        siteActions = actions.site_actions
        self.failUnless('css' in siteActions.keys())
        cssAction = siteActions['css']
        self.assertEquals('CSS', cssAction.title)
        self.assertEquals('CSS', cssAction.description)
        self.assertEquals('string:http://www.freecsstemplates.org/', cssAction.url_expr)
        self.assertEquals(('View',), cssAction.permissions)
        self.failUnless(cssAction.visible)
    def testForAddons(self):
        qi = getToolByName(self.portal, 'portal_quickinstaller')
        self.failUnless(qi.isProductInstalled('ipdasite.projectmgmt'), 'Missing ipdasite.projectmgmt')
        self.failUnless(qi.isProductInstalled('ipdasite.theme'))
        self.failUnless(qi.isProductInstalled('ipdasite.services'))
        self.failUnless(qi.isProductInstalled('ipdasite.views'))
        typesTool = getToolByName(self.portal, 'portal_types')
        types = typesTool.objectIds()
        self.failUnless('IPDA Home' in types)
        self.failUnless('IPDA Event' in types, 'Missing IPDA Event')
    def testIfThemeInstalled(self):
        skins = getToolByName(self.portal, 'portal_skins')
        self.assertEquals('IPDA Theme', skins.getDefaultSkin())
        layer = skins.getSkinPath('IPDA Theme')
        self.failUnless('ipdasite_theme_custom_templates' in layer)
        self.assertEquals('IPDA Theme', skins.getDefaultSkin())

class UpgradeTest(unittest.TestCase):
    '''Test the upgrade steps.'''
    def testHomePageHTML(self):
        from ipdasite.policy.upgrades import _ipdaHomeBody
        self.failUnless('generic-ipda-splash' in _ipdaHomeBody, 'Wrong image in home page')


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
