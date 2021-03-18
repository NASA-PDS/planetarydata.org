# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''IPDA Site Theme — Agencies Viewlet'''

from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter

class AgenciesViewlet(ViewletBase):
    '''Viewlet for rendering logos for the member agencies of the IPDA.'''
    index = ViewPageTemplateFile('agencies.pt')
    def update(self):
        contextState = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
        self.agencies = contextState.actions('ipda_member_agencies')
