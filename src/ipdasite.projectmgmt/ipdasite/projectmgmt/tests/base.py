# encoding: utf-8
# Copyright 2008 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''IPDA Site Project Management: test harness base classes.'''

from App.Common import package_home
from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.MailHost.interfaces import IMailHost
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.SecureMailHost.SecureMailHost import SecureMailHost
from Testing import ZopeTestCase as ztc
from zope.component import getSiteManager

# Traditional Products we have to load manually for test cases:
# (none at this time)

@onsetup
def setupIPDAProjectMgmt():
    '''Set up additional products required for the IPDA Project Management.'''
    fiveconfigure.debug_mode = True
    import ipdasite.projectmgmt
    zcml.load_config('configure.zcml', ipdasite.projectmgmt)
    fiveconfigure.debug_mode = False
    ztc.installPackage('ipdasite.projectmgmt')

setupIPDAProjectMgmt()
ptc.setupPloneSite(products=['ipdasite.projectmgmt'])

class IPDAProjectMgmtTestCase(ptc.PloneTestCase):
    '''Base for tests in this package.'''
    pass
    

class DummyMailHost(SecureMailHost):
    '''Fake mail host for testing email actions.'''
    meta_type = 'Dummy secure mail host'
    def __init__(self, id):
        self.id = id
        self.sent = []
    def _send(self, mfrom, mto, messageText, debug=False):
        self.sent.append(messageText)
    
    

class IPDAProjectMgmtFunctionalTestCase(ptc.FunctionalTestCase):
    '''Base class for functional (doc-)tests.'''
    def afterSetUp(self):
        super(IPDAProjectMgmtFunctionalTestCase, self).afterSetUp()
        self.loginAsPortalOwner()
        sm = getSiteManager(self.portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(DummyMailHost('tester'), IMailHost)
    
    

PACKAGE_HOME = package_home(globals())
