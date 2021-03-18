# encoding: utf-8
# Copyright 2008 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.
'''
IPDA Site Project Management: view for a Project Folder
'''

from Acquisition import aq_inner
from DateTime import DateTime
from ipdasite.projectmgmt.interfaces import IIPDAProject
from plone.memoize.instance import memoize
from Products.ATContentTypes.interface.event import IATEvent
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ProjectFolderView(BrowserView):
    '''Default view for a project folder.'''
    __call__ = ViewPageTemplateFile('templates/projectfolder.pt')
    
    def _getProjects(self, active=False):
    	'''Get projects contained in this folder.  If active is true, get just
    	active ones.  Otherwise, get only inactive ones.'''
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(
            object_provides=IIPDAProject.__identifier__,
            path=dict(query='/'.join(context.getPhysicalPath()), depth=1),
            sort_on='sortable_title',
            active=active
        )
        return [dict(url=i.getURL(), title=i.Title, desc=i.Description, chair=i.chairPerson) for i in results]
    
    @memoize
    def getActiveProjects(self):
        return self._getProjects(active=True)
    
    @memoize
    def getInactiveProjects(self):
        return self._getProjects(active=False)
    
    @memoize
    def getPastEvents(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(
            end={'query': DateTime(), 'range': 'max'},
            object_provides=IATEvent.__identifier__,
            path='/'.join(context.getPhysicalPath()),
            review_state='published',
            sort_limit=10,
            sort_on='start',
            sort_order='reverse'
        )
        return [dict(url=i.getURL(), title=i.Title, desc=i.Description, start=i.start, end=i.end, loc=i.location) for i in results]
    
