# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''IPDA Site Theme: tests of the setup this package applies to a portal site.'''

from ipdasite.theme.testing import IPDA_SITE_THEME_INTEGRATION_TESTING
from lxml import etree
from StringIO import StringIO
import unittest2 as unittest
import os, pkg_resources, re

class SetUpTest(unittest.TestCase):
    '''Set Up Test.'''
    layer = IPDA_SITE_THEME_INTEGRATION_TESTING
    def setUp(self):
        super(SetUpTest, self).setUp()
        self.portal = self.layer['portal']
    def testDisabledAutoComplete(self):
        '''JPL's anal-retentive security scan wants 'autocomplete="off"' on password fields.
        It's not even a standard HTML attribute!
        '''
        for formName in ('login_form', 'login_password', 'failsafe_login_form'):
            loginFormText = self.portal.restrictedTraverse(formName)()
            parser = etree.HTMLParser()
            loginForm = etree.parse(StringIO(loginFormText), parser)
            index = 0
            for field in loginForm.xpath('//input[@type="password"]'):
                index += 1
                autoCompleteSetting = field.get('autocomplete')
                self.assertEquals('off', autoCompleteSetting,
                    '"autocomplete" is not set to "off" for password field #%d on form %s' % (index, formName))
    def testLogo(self):
        '''IPDA-2 reported that the Plone logo still appeared.  Ensure it's actually the IPDA logo.'''
        expected = os.path.getsize(pkg_resources.resource_filename('ipdasite.theme',
            '/skins/ipdasite_theme_custom_images/logo.png'))
        logo = self.portal.unrestrictedTraverse('logo.png')
        self.assertEquals(expected, logo.get_size(), 'IPDA logo not appearing')
    def testShiftedGlobalNav(self):
        '''IPDA-32 reports that the global navigation tabs overlap the site logo.  Make sure it doesn't do that.'''
        overlay = pkg_resources.resource_string('ipdasite.theme', '/static/ipda-overlay.css')
        self.failUnless(re.search(r'#header\s*{\s*height:\s?11em;', overlay), 'Override for #header height missing')
        self.failUnless(re.search(r'#menu\s*{\s*top:\s?8em', overlay), 'Override for #menu top missing')

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

