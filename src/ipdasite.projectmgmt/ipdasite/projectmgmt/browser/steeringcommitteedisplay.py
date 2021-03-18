# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.
'''
IPDA Site Project Management: view for the Steering Committee Display
'''

from Acquisition import aq_inner
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from urllib import quote_plus
from zope.component import getMultiAdapter

class SteeringCommitteeDisplayView(BrowserView):
    '''Default view for a Steering Committee Display.'''
    __call__ = ViewPageTemplateFile('templates/steeringcommitteedisplay.pt')
    def _getPortalState(self):
        return getMultiAdapter((aq_inner(self.context), self.request), name=u'plone_portal_state')

    @memoize
    def anonymous(self):
        return self._getPortalState().anonymous()

    @memoize
    def prefPage(self):
        ps = self._getPortalState()
        return u'%s/personalize_form' % ps.portal_url()
        
    @memoize
    def scMembers(self):
        memberTool = getToolByName(aq_inner(self.context), 'portal_membership')
        members = memberTool.searchForMembers(groupname='SC')
        members.sort(lambda a, b: cmp(a.getId(), b.getId()))
        portalURL = self._getPortalState().portal_url()
        return [dict(
            url=u'%s/author/%s' % (portalURL, quote_plus(i.getId())),
            name=i.getProperty('fullname', i.getId()),
            institution=i.getProperty('institution', ''),
        ) for i in members]

    @memoize
    def tegMembers(self):
        memberTool = getToolByName(aq_inner(self.context), 'portal_membership')
        members = memberTool.searchForMembers(groupname='TEG')
        members.sort(lambda a, b: cmp(a.getId(), b.getId()))
        portalURL = self._getPortalState().portal_url()
        return [dict(
            url=u'%s/author/%s' % (portalURL, quote_plus(i.getId())),
            name=i.getProperty('fullname', i.getId()),
            institution=i.getProperty('institution', ''),
        ) for i in members]
