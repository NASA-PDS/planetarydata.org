# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''IPDA Project Management Portlets: Events portlet.
'''

from Acquisition import aq_inner
from DateTime import DateTime
from ipdasite.projectmgmt import IPDAMessageFactory as _
from ipdasite.projectmgmt.interfaces import IIPDAEvent
from plone.memoize.instance import memoize
from Products.ATContentTypes.interface.event import IATEvent
from Products.CMFCore.utils import getToolByName
from zope.formlib import form
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.app.portlets.cache import render_cachekey
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.portlets.interfaces import IPortletDataProvider
from zope import schema

class IEventsPortlet(IPortletDataProvider):
    count = schema.Int(
        title=_(u'Number of items to display'),
        description=_(u'How many items to list.'),
        required=True,
        default=5
    )
    state = schema.Tuple(
        title=_(u'Workflow state'),
        description=_(u'Items in which workflow state to show.'),
        default=('published',),
        required=True,
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.WorkflowStates')
        )

class Assignment(base.Assignment):
    implements(IEventsPortlet)
    def __init__(self, count=5, state=('published',)):
        self.count = count
        self.state = state
    @property
    def title(self):
        return _(u'IPDA Events')

class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('events.pt')
    def __init__(self, *args):
        super(Renderer, self).__init__(*args)
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        self.portal_url = portal_state.portal_url()
        self.portal = portal_state.portal()
        self.have_events_folder = 'events' in self.portal.objectIds()
    @ram.cache(render_cachekey)
    def render(self):
        return xhtml_compress(self._template())
    @property
    def available(self):
        return len(self._data())
    def published_events(self):
        return self._data()
    def all_events_link(self):
        if self.have_events_folder:
            return '%s/events' % self.portal_url
        else:
            return '%s/events_listing' % self.portal_url
    def prev_events_link(self):
        if (self.have_events_folder and
            'aggregator' in self.portal['events'].objectIds() and
            'previous' in self.portal['events']['aggregator'].objectIds()):
            return '%s/events/aggregator/previous' % self.portal_url
            
        elif (self.have_events_folder and
            'previous' in self.portal['events'].objectIds()):
            return '%s/events/previous' % self.portal_url
        else:
            return None
    @memoize
    def _data(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        limit = self.data.count
        state = self.data.state
        return catalog(
            object_provides=(IATEvent.__identifier__, IIPDAEvent.__identifier__),
            review_state=state,
            end={'query': DateTime(), 'range': 'min'},
            sort_on='start',
            sort_limit=limit,
        )[:limit]
    
class AddForm(base.AddForm):
    form_fields = form.Fields(IEventsPortlet)
    label = _(u'Add IPDA Events Portlet')
    description = _(u'This portlet lists upcoming IPDA Events and other Events.')
    def create(self, data):
        return Assignment(count=data.get('count', 5), state=data.get('state', ('published',)))

class EditForm(base.EditForm):
    form_fields = form.Fields(IEventsPortlet)
    label = _(u'Edit IPDA Events Portlet')
    description = _(u'This portlet lists upcoming Events.')
