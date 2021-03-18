# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Specification Link: implementation'''

from Acquisition import aq_inner, aq_parent
from ipdasite.services import ProjectMessageFactory as _
from ipdasite.services.config import PROJECTNAME
from ipdasite.services.interfaces import ISpecificationLink
from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from zope.interface import implements
from archetypes.referencebrowserwidget import ReferenceBrowserWidget
import pds.registry.model, registryobject

SpecificationLinkSchema = registryobject.RegistryObjectSchema.copy() + atapi.Schema((
    atapi.ReferenceField(
        'specificationObject',
        relationship='specifiedIn',
        multiValued=False,
        required=False,
        storage=atapi.AnnotationStorage(),
        widget=ReferenceBrowserWidget(
            label=_(u'Specification Object'),
            description=_(u'Object that provides the technical specification for a service binding.'),
            startup_directory='/',
        ),
    ),
    atapi.StringField(
        'usageDescription',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextAreaWidget(
            label=_(u'Usage Description'),
            description=_(u'Tells how to use the optional usage parameters'),
        ),
    ),
    atapi.LinesField(
        'usageParameters',
        multiValued=True,
        required=False,
        searchable=False,
        storage=atapi.AnnotationStorage(),
        widget=atapi.LinesWidget(
            label=_(u'Usage Parameters'),
            description=_(u'Instance-specific parameters telling how to use the technical specification, one per line.'),
        ),
    ),
))

SpecificationLinkSchema['title'].storage = atapi.AnnotationStorage()
SpecificationLinkSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(SpecificationLinkSchema, folderish=True, moveDiscussion=False)

class SpecificationLink(registryobject.RegistryObject):
    '''Provides the linkage between a Service Binding and its technical specification.'''
    implements(ISpecificationLink)
    schema              = SpecificationLinkSchema
    portal_type         = 'Specification Link'
    description         = atapi.ATFieldProperty('description')
    specificationObject = atapi.ATReferenceFieldProperty('specificationObject')
    title               = atapi.ATFieldProperty('title')
    usageDescription    = atapi.ATFieldProperty('usageDescription')
    usageParameters     = atapi.ATFieldProperty('usageParameters')
    def toPDSRegistry(self):
        binding = aq_parent(aq_inner(self))
        specURL = self.specificationObject is not None and self.specificationObject.absolute_url() or None
        params = self.usageParameters and list(self.usageParameters) or None
        return pds.registry.model.SpecificationLink(
            self.guid, self.lid, binding.guid, specURL, self.home, set(), self.title, 'accepted', self.description,
            versionName=self.versionID, usageDescription=self.usageDescription, usageParameters=params
        )

atapi.registerType(SpecificationLink, PROJECTNAME)
