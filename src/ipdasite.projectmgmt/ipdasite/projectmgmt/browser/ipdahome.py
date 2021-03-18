# encoding: utf-8
# Copyright 2008 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.
'''
IPDA Site Project Management: view for the IPDA home page
'''

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Acquisition import aq_inner
from plone.memoize.instance import memoize
from Products.ATContentTypes.interface.event import IATEvent
from DateTime import DateTime
from urllib import quote_plus
from zope.component import getMultiAdapter

class IPDAHomeView(BrowserView):
    '''Default view for an IPDA welcome page.'''
    __call__ = ViewPageTemplateFile('templates/ipdahome.pt')

    def _getPortalState(self):
        return getMultiAdapter((self.context, self.request), name=u'plone_portal_state')

    @memoize
    def getLoginURL(self):
        return self._getPortalState().portal_url() + '/login_form'

    @memoize
    def getUserName(self):
        tools = getMultiAdapter((self.context, self.request), name=u'plone_tools')
        member = self._getPortalState().member()
        userID = member.getId()
        memberInfo = tools.membership().getMemberInfo(userID)
        if memberInfo:
            return memberInfo.get('fullname', '')
        else:
            return userID
    
    @memoize
    def getUserLink(self):
        portalState = self._getPortalState()
        member = portalState.member()
        return '%s/author/%s' % (portalState.portal_url(), quote_plus(member.getId()))
    
    @memoize
    def getNextEvents(self):
        context = aq_inner(self)
        catalog = getToolByName(context, 'portal_catalog')
        return catalog(
            object_provides=IATEvent.__identifier__,
            end={'query': DateTime(), 'range': 'min'},
            sort_on='start',
            sort_limit=2,
            review_state='published'
        )[:2]
    
