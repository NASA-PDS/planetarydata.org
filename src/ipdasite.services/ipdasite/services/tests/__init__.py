# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''IPDA Service Registry: tests'''

import unittest
import testDocs, testSetup

def test_suite():
    return unittest.TestSuite([
        testDocs.test_suite(),
        testSetup.test_suite(),
        
        # Unit tests
        # doctestunit.DocFileSuite(
        #    'README.txt', package='ipdasite.service',
        #    setUp=testing.setUp, tearDown=testing.tearDown),
        # 
        #doctestunit.DocTestSuite(
        #    module='ipdasite.service.mymodule',
        #    setUp=testing.setUp, tearDown=testing.tearDown),


        # Integration tests that use PloneTestCase
        #ztc.ZopeDocFileSuite(
        #    'README.txt', package='ipdasite.service',
        #    test_class=TestCase),

        #ztc.FunctionalDocFileSuite(
        #    'browser.txt', package='ipdasite.service',
        #    test_class=TestCase),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
