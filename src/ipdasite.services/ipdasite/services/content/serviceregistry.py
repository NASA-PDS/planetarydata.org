# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

# + add service to registry
# + delete service from registry
# + move service in registry (but not really needed)
# + move service between registries
# + edit service
# + edit registry home URL
# + add binding to service (handled with declaration to container modified)
# + remove binding from service (ibid)
# + move binding in service (ibid)
# + move binding between services (ibid)
# + edit binding
# + add link to binding (handled with declaration to container modified)
# + remove link from binding (ibid)
# + move link in binding (ibid)
# + move link between bindings (ibid)
# edit link
# periodic sync
# + edit curator
# + delete curator (handled with declaration to container modified)

'''Service Registry: implementation'''

from Acquisition import aq_inner, aq_parent
from ipdasite.services import ProjectMessageFactory as _
from ipdasite.services.config import PROJECTNAME
from ipdasite.services.interfaces import IServiceRegistry
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from Products.CMFCore.interfaces import ISiteRoot
from zope.interface import implements
from pds.registry.net import PDSRegistryClient
from pds.registry.model import areServicesIdentical
from Products.CMFCore.utils import getToolByName
import logging, threading, urllib2

_logger = logging.getLogger(__name__)

ServiceRegistrySchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.StringField(
        'home',
        required=True,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        validators=('isURL',),
        widget=atapi.StringWidget(
            label=_(u'Home'),
            description=_(u'Base URI of the registry.'),
         ),
    ),
    atapi.BooleanField(
        'sync',
        required=False,
        storage=atapi.AnnotationStorage(),
        widget=atapi.BooleanWidget(
            label=_(u'Synchronize'),
            description=_(u'Enable synchronization with a PDS Registry Service at the home URL.'),
        ),
    ),
))
ServiceRegistrySchema['title'].storage = atapi.AnnotationStorage()
ServiceRegistrySchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(ServiceRegistrySchema, folderish=True, moveDiscussion=False)

class ServiceRegistry(folder.ATFolder):
    '''A registry that contains definitions of services.'''
    implements(IServiceRegistry)
    schema      = ServiceRegistrySchema
    portal_type = 'Service Registry'
    description = atapi.ATFieldProperty('description')
    home        = atapi.ATFieldProperty('home')
    title       = atapi.ATFieldProperty('title')
    sync        = atapi.ATFieldProperty('sync')
    _lock       = threading.RLock()
    def synchronize(self):
        if not self.sync: return
        myPath = '/'.join(self.getPhysicalPath())
        try:
            _logger.info('Sync requested for %s', myPath)
            if not self._lock.acquire(blocking=False):
                _logger.info('Another thread has already locked %s, so ignoring this sync request', myPath)
                return
            self._doSync()
            _logger.info('Sync completed for %s', myPath)
        finally:
            self._lock.release()
    def _describeMyServices(self):
        myServices = {}
        for key in self.keys():
            child = self[key]
            if child.portal_type != 'Service': continue
            myServices[child.guid] = child.toPDSRegistry()
        return myServices
    def _doSync(self):
        try:
            prc = PDSRegistryClient(self.home)
            pdsServices = dict([(i.guid, i) for i in prc.getServices()])
            myServices = self._describeMyServices()
            toPut = []
            for myGUID, myService in myServices.iteritems():
                if myGUID not in pdsServices:
                    toPut.append(myService)
                else:
                    pdsService = pdsServices[myGUID]
                    del pdsServices[myGUID]
                    if not areServicesIdentical(myService, pdsService):
                        toPut.append(myService)
            for guid in pdsServices.keys():
                prc.deleteService(guid)
            for service in toPut:
                prc.putService(service)
        except urllib2.HTTPError:
            _logger.exception('Problem communicating with PDS Registry Service at %s', self.home)
            utils = getToolByName(self, 'plone_utils')
            utils.addPortalMessage(
                _(u'Problem communicating with PDS Registry Service; information not synchronized at this time.')
            )

atapi.registerType(ServiceRegistry, PROJECTNAME)

def syncServiceRegistry(context, event):
    item = aq_inner(context)
    while not IServiceRegistry.providedBy(item):
        if ISiteRoot.providedBy(item):
            # Traveled upward and found *no* service registry? This shouldn't happen,
            # but if it does, log it, and we're done.
            _logger.warning('Event %r for %s, but no IServiceRegistry parent found', event, '/'.join(context.getPhysicalPath()))
            return
        item = aq_parent(item)
    item.synchronize()

