# encoding: utf-8
# Copyright 2008 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
IPDA Site Project Management: IPDA Home Page
'''

from ipdasite.projectmgmt.config import PROJECTNAME
from ipdasite.projectmgmt.interfaces import IIPDAHome
from Products.Archetypes import atapi
from Products.ATContentTypes.content import document
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from zope.interface import implements

IPDAHomeSchema = document.ATDocumentSchema.copy() + atapi.Schema((
    # No other fields
))
IPDAHomeSchema['title'].storage = atapi.AnnotationStorage()
IPDAHomeSchema['description'].storage = atapi.AnnotationStorage()
IPDAHomeSchema['text'].storage = atapi.AnnotationStorage()
IPDAHomeSchema['presentation'].storage = atapi.AnnotationStorage()
IPDAHomeSchema['tableContents'].storage = atapi.AnnotationStorage()
finalizeATCTSchema(IPDAHomeSchema, folderish=False, moveDiscussion=True)

class IPDAHome(document.ATDocument):
    '''Home page for the International Planetary Data Alliance.'''
    implements(IIPDAHome)
    portal_type               = 'IPDA Home'
    _at_rename_after_creation = True
    schema                    = IPDAHomeSchema
    title                     = atapi.ATFieldProperty('title')
    description               = atapi.ATFieldProperty('description')
    text                      = atapi.ATFieldProperty('text')
    presentation              = atapi.ATFieldProperty('presentation')
    tableContents             = atapi.ATFieldProperty('tableContents')
    

atapi.registerType(IPDAHome, PROJECTNAME)