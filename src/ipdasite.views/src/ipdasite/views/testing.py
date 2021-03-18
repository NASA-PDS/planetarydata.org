# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''IPDA Site Views: testing fixtures.'''

from plone.testing import z2
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting

class IPDASiteViews(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)
    def setUpZope(self, app, configurationContext):
        import ipdasite.views
        self.loadZCML(package=ipdasite.views)
    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'ipdasite.views:default')
    
IPDA_SITE_VIEWS = IPDASiteViews()
IPDA_SITE_VIEWS_INTEGRATION_TESTING = IntegrationTesting(bases=(IPDA_SITE_VIEWS,), name='IPDASiteViews:Integration')
IPDA_SITE_VIEWS_FUNCTIONAL_TESTING = FunctionalTesting(bases=(IPDA_SITE_VIEWS,), name='IPDASiteViews:Functional')
