# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Service: implementation'''

from ipdasite.services import ProjectMessageFactory as _
from ipdasite.services.config import PROJECTNAME
from ipdasite.services.interfaces import IService
from Products.Archetypes import atapi
from Products.ATContentTypes.content import folder
from Products.ATContentTypes.content import schemata
from zope.interface import implements, directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
import pds.registry.model, registryobject

_operatingSystems = (
    (_(u'AIX'), u'AIX'),
    (_(u'Android'), u'Android'),
    (_(u'BeOS'), u'BeOS'),
    (_(u'BSD Unix'), u'BSD Unix'),
    (_(u'GNU Hurd'), u'GNU Hurd'),
    (_(u'HP-UX'), u'HP-UX'),
    (_(u'iOS'), u'iOS'),
    (_(u'IRIX'), u'IRIX'),
    (_(u'Linux'), u'Linux'),
    (_(u'Mac OS 9'), u'Mac OS 9'),
    (_(u'Mac OS X'), u'Mac OS X'),
    (_(u'MS-DOS'), u'MS-DOS'),
    (_(u'MS-Windows'), u'MS-Windows'),
    (_(u'OS Independent'), u'OS Independent'),
    (_(u'OS/2'), u'OS/2'),
    (_(u'PalmOS'), u'PalmOS'),
    (_(u'Solaris'), u'Solaris'),
    (_(u'Other OS'), u'Other OS'),
    (_(u'Other Unix'), u'Other Unix'),
)

_interfaceTypes = (
    (_(u'API'), u'API'),
    (_(u'Console'), u'Console'),
    (_(u'GUI'), u'GUI'),
    (_(u'Script'), u'Script'),
    (_(u'Service'), u'Service'),
)

_serviceCategories = (
    (_(u'Analysis'), u'Analysis'),
    (_(u'Data reader'), u'Data reader'),
    (_(u'Design'), u'Design'),
    (_(u'Dissemination'), u'Dissemination'),
    (_(u'Generation'), u'Generation'),
    (_(u'Planning'), u'Planning'),
    (_(u'Search & retrieval'), u'Search/retrieve'),
    (_(u'Validation'), u'Validation'),
    (_(u'Visualization'), u'Visualization'),
)

ServiceSchema = registryobject.RegistryObjectSchema.copy() + folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.StringField(
        'toolURL',
        required=False,
        storage=atapi.AnnotationStorage(),
        validators=('isURL',),
        widget=atapi.StringWidget(
            label=_(u'Tool URL'),
            description=_(u'URL to the tool described by this "service".'),
        )
    ),
    atapi.DateTimeField(
        'releaseDate',
        required=False,
        storage=atapi.AnnotationStorage(),
        widget=atapi.CalendarWidget(
            label=_(u'Release Date'),
            description=_(u'Date of latest release.'),
            show_hm=False,
        ),
    ),
    atapi.LinesField(
        'categories',
        required=False,
        storage=atapi.AnnotationStorage(),
        enforceVocabulary=True,
        vocabulary_factory=u'ipdasite.services.ServiceCategories',
        widget=atapi.PicklistWidget(
            label=_(u'Category'),
            description=_(u'One or more terms used to group tools.'),
        ),
    ),
    atapi.LinesField(
        'interfaceTypes',
        required=False,
        storage=atapi.AnnotationStorage(),
        enforceVocabulary=True,
        multiValued=True,
        vocabulary_factory=u'ipdasite.services.InterfaceTypes',
        widget=atapi.MultiSelectionWidget(
            label=_(u'Interface Types'),
            description=_(u'Types of interface presented by the service and/or tool.'),
            format='checkbox',
        ),
    ),
    atapi.TextField(
        'abstract',
        required=False,
        storage=atapi.AnnotationStorage(),
        searchable=True,
        validators=('isTidyHtmlWithCleanup',),
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(
            label=_(u'Abstract'),
            description=_(u'A longer summary than a mere description that tells a lot more about the service (but not too long).'),
            rows=12,
            allow_file_upload=False,
        ),
    ),
    atapi.LinesField(
        'operatingSystems',
        required=False,
        storage=atapi.AnnotationStorage(),
        enforceVocabulary=True,
        vocabulary_factory=u'ipdasite.services.OperatingSystems',
        widget=atapi.PicklistWidget(
            label=_(u'Operating Systems'),
            description=_(u'Computer platforms on which the service is available, if applicable'),
        ),
    ),
    atapi.TextField(
        'requirements',
        required=False,
        storage=atapi.AnnotationStorage(),
        searchable=True,
        widget=atapi.TextAreaWidget(
            label=_(u'Requirements'),
            description=_(u'Any special pre-requisites that must be met before using this service.'),
            rows=12,
            allow_file_upload=False,
        ),
    ),
    atapi.ReferenceField(
        'curator',
        relationship='curatedBy',
        multiValued=False,
        required=False,
        storage=atapi.AnnotationStorage(),
        vocabulary_factory=u'ipdasite.services.Curators',
        vocabulary_display_path_bound=-1,
        widget=atapi.ReferenceWidget(
            label=_(u'Curator'),
            description=_(u'Agency responsible for this service.'),
        ),
    ),
))

ServiceSchema['title'].storage = atapi.AnnotationStorage()
ServiceSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(ServiceSchema, folderish=True, moveDiscussion=False)

class Service(folder.ATFolder, registryobject.RegistryObject):
    '''A service that provides a use for external software.'''
    implements(IService)
    schema           = ServiceSchema
    portal_type      = 'Service'
    abstract         = atapi.ATFieldProperty('abstract')
    categories       = atapi.ATFieldProperty('categories')
    curator          = atapi.ATReferenceFieldProperty('curator')
    description      = atapi.ATFieldProperty('description')
    interfaceTypes   = atapi.ATFieldProperty('interfaceTypes')
    operatingSystems = atapi.ATFieldProperty('operatingSystems')
    releaseDate      = atapi.ATFieldProperty('releaseDate')
    requirements     = atapi.ATFieldProperty('requirements')
    title            = atapi.ATFieldProperty('title')
    toolURL          = atapi.ATFieldProperty('toolURL')
    def toPDSRegistry(self):
        slots = set()
        if self.curator:
            slots.add(pds.registry.model.Slot(u'curator-name', [self.curator.title], 'unicode'))
            for fieldName in ('description', 'contactName', 'emailAddress', 'telephone'):
                value = getattr(self.curator, fieldName, None)
                if value:
                    slots.add(pds.registry.model.Slot(u'curator-%s' % fieldName, [value], 'unicode'))
        for fieldName in ('abstract', 'requirements', 'toolURL'):
            value = getattr(self, fieldName, None)
            if value:
                slots.add(pds.registry.model.Slot(unicode(fieldName), [value], 'unicode'))
        for fieldName in ('categories', 'interfaceTypes', 'operatingSystems'):
            value = getattr(self, fieldName, None)
            if value:
                slots.add(pds.registry.model.Slot(unicode(fieldName), list(value)))
        if self.releaseDate:
            slots.add(pds.registry.model.Slot(u'releaseDate', [unicode(self.releaseDate)], 'date'))
        s = pds.registry.model.Service(
            self.guid, self.lid, self.home, slots, self.title, 'accepted', self.description,
            versionName=self.versionID
        )
        for i in self.keys():
            bindingObj = self[i]
            s.serviceBindings.add(bindingObj.toPDSRegistry())
        return s

atapi.registerType(Service, PROJECTNAME)

def ServiceCategoryVocabulary(context):
    return SimpleVocabulary.fromItems(_serviceCategories)
directlyProvides(ServiceCategoryVocabulary, IVocabularyFactory)

def OperatingSystemsVocabulary(context):
    return SimpleVocabulary.fromItems(_operatingSystems)
directlyProvides(OperatingSystemsVocabulary, IVocabularyFactory)

def InterfaceTypesVocabulary(context):
    return SimpleVocabulary.fromItems(_interfaceTypes)
directlyProvides(InterfaceTypesVocabulary, IVocabularyFactory)
