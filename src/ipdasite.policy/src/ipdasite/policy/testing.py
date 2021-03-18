# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''IPDA Site Policy: testing fixtures.'''

from ipdasite.theme.testing import IPDA_SITE_THEME
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2
from Products.CMFCore.utils import getToolByName


class IPDASitePolicy(PloneSandboxLayer):
    defaultBases = (IPDA_SITE_THEME,)
    def setUpZope(self, app, configurationContext):
        import ipdasite.policy
        self.loadZCML(package=ipdasite.policy)
    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'ipdasite.policy:default')
        wfTool = getToolByName(portal, 'portal_workflow')
        wfTool.setDefaultChain('plone_workflow')
    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'ipdasite.policy')


IPDA_SITE_POLICY = IPDASitePolicy()
IPDA_SITE_POLICY_INTEGRATION_TESTING = IntegrationTesting(bases=(IPDA_SITE_POLICY,), name='IPDASitePolicy:Integration')
IPDA_SITE_POLICY_FUNCTIONAL_TESTING = FunctionalTesting(bases=(IPDA_SITE_POLICY,), name='IPDASitePolicy:Functional')
