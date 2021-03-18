# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Synchronize with a PDS Registry Service.'''

from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from ipdasite.services.interfaces import IServiceRegistry
import logging

_logger = logging.getLogger(__name__)
    
class PortalWideRegistrySyncer(BrowserView):
    '''Synchronizer for all local Registries'''
    def __call__(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(object_provides=IServiceRegistry.__identifier__)
        # We're gonna have to wake these objects to sync 'em, so no big deal:
        registries = [i.getObject() for i in results if i.getObject().sync]
        # No registries want syncing?
        numRegistries = len(registries)
        if numRegistries == 0: return
        _logger.info('Sync all registries, number to sync: %d', numRegistries)
        for reg in registries:
            reg.synchronize()
        _logger.info('Completed sync of all registries (%d)', numRegistries)
    
