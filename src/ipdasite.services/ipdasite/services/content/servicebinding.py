# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Service Binding: implementation'''

from Acquisition import aq_inner, aq_parent
from ipdasite.services import ProjectMessageFactory as _
from ipdasite.services.config import PROJECTNAME
from ipdasite.services.interfaces import IServiceBinding
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from zope.interface import implements
import pds.registry.model, registryobject

ServiceBindingSchema = registryobject.RegistryObjectSchema.copy() + folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.StringField(
        'accessURI',
        required=False,
        searchable=False,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'Access URI'),
            description=_(u'URI that identifies the endpoint where the service may be accessed'),
            size=50,
        ),
    ),
))

ServiceBindingSchema['title'].storage = atapi.AnnotationStorage()
ServiceBindingSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(ServiceBindingSchema, folderish=True, moveDiscussion=False)

class ServiceBinding(folder.ATFolder, registryobject.RegistryObject):
    '''A service binding identifies the endpoint and specifications for a service.'''
    implements(IServiceBinding)
    schema      = ServiceBindingSchema
    portal_type = 'Service Binding'
    accessURI   = atapi.ATFieldProperty('accessURI')
    description = atapi.ATFieldProperty('description')
    title       = atapi.ATFieldProperty('title')
    def toPDSRegistry(self):
        service = aq_parent(aq_inner(self))
        b = pds.registry.model.ServiceBinding(
            self.guid, self.lid, service.guid, self.home, set(), self.title, 'accepted', self.description,
            versionName=self.versionID, accessURI=self.accessURI, specificationLinks=None, targetBinding=None
        )
        for i in self.keys():
            specificationLink = self[i]
            b.specificationLinks.add(specificationLink.toPDSRegistry())
        return b

atapi.registerType(ServiceBinding, PROJECTNAME)
