# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
IPDA Site Project Management: IPDA Content
'''

from ipdasite.projectmgmt import IPDAMessageFactory as _
from ipdasite.projectmgmt.interfaces import IIPDAContent
from Products.Archetypes import atapi
from Products.ATContentTypes.content.schemata import finalizeATCTSchema, ATContentTypeSchema
from zope.interface import implements
from Products.ATContentTypes.content import base

_description = _(u'Enter the IPDA document ID including working group (WKG), document type (DT), number (NNN), version (V),' \
    + 'revision (R), date (YYYYMMMDD) and name (NAME). Use the "Title" field to give a more readable name.')

IPDAContentSchema = ATContentTypeSchema.copy() + atapi.Schema((
    atapi.StringField(
        'documentID',
        default=u'IPDA-WKG-DT-NNN_V_R_YYYYMMMDD-NAME',
        required=True,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'IPDA Document ID'),
            description=_description,
            size=50,
        ),
    ),
))

finalizeATCTSchema(IPDAContentSchema, folderish=False, moveDiscussion=True)

class IPDAContent(base.ATCTContent):
    '''Abstract IPDA content.'''
    implements(IIPDAContent)
    schema = IPDAContentSchema
    documentID = atapi.ATFieldProperty('documentID')
