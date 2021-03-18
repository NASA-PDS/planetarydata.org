# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Registry Object: implementation'''

from ipdasite.services import ProjectMessageFactory as _
from ipdasite.services.interfaces import IRegistryObject
from Products.Archetypes import atapi
from Products.Archetypes.interfaces import IObjectPostValidation
from Products.ATContentTypes.content import schemata
from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.utils import getToolByName
import identifiable

RegistryObjectSchema = identifiable.IdentifiableSchema.copy() + atapi.Schema((
    atapi.StringField(
        'lid',
        required=True,
        searchable=False,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'LID'),
            description=_(u'Logical Identifier'),
            size=50,
        ),
    ),
    atapi.StringField(
        'versionID',
        required=True,
        searchable=False,
        default=u'0.0.0',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'Version ID'),
            description=_(u'The version of this object (as chosen by the object registrant).'),
        ),
    ),
    # title & description also appear in IServiceRegistry, but they come for free from identifiable's schema
))

schemata.finalizeATCTSchema(RegistryObjectSchema, folderish=False, moveDiscussion=False)

class RegistryObject(identifiable.Identifiable):
    '''An registry object, in the ebXML registry sense.'''
    implements(IRegistryObject)
    schema      = RegistryObjectSchema
    description = atapi.ATFieldProperty('description')
    lid         = atapi.ATFieldProperty('lid')
    title       = atapi.ATFieldProperty('title')
    versionID   = atapi.ATFieldProperty('versionID')

# We don't register this class because it's used solely as an abstract base
# for Service, ServiceBinding, etc. and we don't expect instances of this class
# to ever exist.

class LogicalIDUniquenessValidator(object):
    '''Validator to ensure that logical identifiers are unique system-wide.'''
    implements(IObjectPostValidation)
    adapts(IRegistryObject)
    def __init__(self, context):
        self.context = context
    def __call__(self, request):
        value = request.form.get('lid', request.get('lid', None))
        if value is not None:
            catalog = getToolByName(self.context, 'portal_catalog')
            results = catalog(lid=value, object_provides=IRegistryObject.__identifier__)
            if len(results) == 0:
                return None
            elif len(results) == 1 and results[0].UID == self.context.UID():
                return None
            else:
                return {'lid': _(u'The logical ID is already in use')}
        return None
    

            
