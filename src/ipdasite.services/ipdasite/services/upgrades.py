# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from Products.CMFCore.utils import getToolByName
from ipdasite.services.interfaces import IService

def _getPortal(setupTool):
    '''Get the portal from the given setup tool context'''
    return getToolByName(setupTool, 'portal_url').getPortalObject()

def nullUpgradeStep(setupTool):
    '''A null step for when a profile upgrade requires no custom activity.'''

def transformToolURLsFromServiceBindings(setupTool):
    '''For profile 3-to-4, we take Service Binding's access URIs and use them in Service objects' "toolURL" fields.'''
    portal = _getPortal(setupTool)
    catalog = getToolByName(portal, 'portal_catalog')
    results = catalog(object_provides=IService.__identifier__)
    for i in results:
        service = i.getObject()
        bindings = service.keys()
        if len(bindings) == 0: continue
        # Arbitrarily pick the first service binding
        service.toolURL = service[bindings[0]].accessURI
        service.reindexObject()
