# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Identifiable: implementation'''

from ipdasite.services import ProjectMessageFactory as _
from ipdasite.services.interfaces import IIdentifiable
from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata, base
from zope.interface import implements
import uuid

IdentifiableSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    atapi.StringField(
        'guid',
        required=True,
        searchable=False,
        default_method='defaultGUID',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'GUID'),
            description=_(u'Globally Unique Identifier.'),
            size=50,
         ),
    ),
))

# title & description appear in IServiceRegistry, a subinterface of IIdentifiable
# but they come "for free" in ATContentTypeSchema, so we'll go ahead and adjust
# their storage here
IdentifiableSchema['title'].storage = atapi.AnnotationStorage()
IdentifiableSchema['description'].storage = atapi.AnnotationStorage()

schemata.finalizeATCTSchema(IdentifiableSchema, folderish=False, moveDiscussion=False)

class Identifiable(base.ATCTContent):
    '''An identifiable object, in the ebXML registry sense.'''
    implements(IIdentifiable)
    schema = IdentifiableSchema
    guid   = atapi.ATFieldProperty('guid')
    def defaultGUID(self):
        '''Yield a default GUID'''
        return u'urn:uuid:' + unicode(uuid.uuid4())

# We don't register this class because it's used solely as an abstract base
# for Service, ServiceBinding, etc. and we don't expect instances of this class
# to ever exist.


