# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.app.theming.testing import THEMING_FIXTURE

class IPDASiteTheme(PloneSandboxLayer):
    '''IPDA Site Theme testing layer.'''
    defaultBases = (THEMING_FIXTURE,)
    def setUpZope(self, app, configurationContext):
        import ipdasite.theme
        self.loadZCML(package=ipdasite.theme)
    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'ipdasite.theme:default')

IPDA_SITE_THEME = IPDASiteTheme()
IPDA_SITE_THEME_INTEGRATION_TESTING = IntegrationTesting(bases=(IPDA_SITE_THEME,), name='IPDASiteTheme:Integration')
IPDA_SITE_THEME_FUNCTIONAL_TESTING = FunctionalTesting(bases=(IPDA_SITE_THEME,), name='IPDASiteTheme:Functional')

