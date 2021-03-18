# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
IPDA Site Project Management: IPDA File
'''

from ipdasite.projectmgmt.config import PROJECTNAME
from ipdasite.projectmgmt.interfaces import IIPDAFile
from ipdasite.projectmgmt.content.ipdacontent import IPDAContent
from Products.Archetypes import atapi
from Products.ATContentTypes.content.file import ATFile, ATFileSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from zope.interface import implements

IPDAFileSchema = ATFileSchema.copy() + IPDAContent.schema.copy() + atapi.Schema((
    # No other fields.
))
finalizeATCTSchema(IPDAFileSchema, folderish=False, moveDiscussion=True)
IPDAFileSchema.moveField('documentID', after='title')

class IPDAFile(IPDAContent, ATFile):
    '''IPDA File.'''
    implements(IIPDAFile)
    portal_type               = 'IPDA File'
    _at_rename_after_creation = True
    schema                    = IPDAFileSchema

atapi.registerType(IPDAFile, PROJECTNAME)
