# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
IPDA Site Project Management: IPDA Document
'''

from ipdasite.projectmgmt.config import PROJECTNAME
from ipdasite.projectmgmt.interfaces import IIPDADocument
from ipdasite.projectmgmt.content.ipdacontent import IPDAContent
from Products.Archetypes import atapi
from Products.ATContentTypes.content import document
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from zope.interface import implements

IPDADocumentSchema = document.ATDocumentSchema.copy() + IPDAContent.schema.copy() + atapi.Schema((
    # No other fields.
))
finalizeATCTSchema(IPDADocumentSchema, folderish=False, moveDiscussion=True)
IPDADocumentSchema.moveField('documentID', after='title')

class IPDADocument(IPDAContent, document.ATDocument):
    '''IPDA Document.'''
    implements(IIPDADocument)
    portal_type               = 'IPDA Document'
    _at_rename_after_creation = True
    schema                    = IPDADocumentSchema

atapi.registerType(IPDADocument, PROJECTNAME)
