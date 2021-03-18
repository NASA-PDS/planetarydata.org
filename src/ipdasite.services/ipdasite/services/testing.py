# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''IPDA Site Services: testing fixtures.'''

from plone.testing import z2
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting
from Products.CMFCore.utils import getToolByName

class IPDASiteServices(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)
    def setUpZope(self, app, configurationContext):
        import ipdasite.services
        self.loadZCML(package=ipdasite.services)
        z2.installProduct(app, 'ipdasite.services')
    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'ipdasite.services:default')
        wfTool = getToolByName(portal, 'portal_workflow')
        wfTool.setDefaultChain('plone_workflow')
    
IPDA_SITE_SERVICES = IPDASiteServices()
IPDA_SITE_SERVICES_INTEGRATION_TESTING = IntegrationTesting(bases=(IPDA_SITE_SERVICES,), name='IPDASiteServices:Integration')
IPDA_SITE_SERVICES_FUNCTIONAL_TESTING = FunctionalTesting(bases=(IPDA_SITE_SERVICES,), name='IPDASiteServices:Functional')
