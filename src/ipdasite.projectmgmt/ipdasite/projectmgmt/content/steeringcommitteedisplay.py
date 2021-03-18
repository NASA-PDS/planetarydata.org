# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''IPDA Project Management: Steering Committee Display.'''

from ipdasite.projectmgmt import IPDAMessageFactory as _
from ipdasite.projectmgmt.config import PROJECTNAME
from ipdasite.projectmgmt.interfaces import ISteeringCommitteeDisplay
from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from zope.interface import implements

SteeringCommitteeDisplaySchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    # No other fields
))
SteeringCommitteeDisplaySchema['title'].storage = atapi.AnnotationStorage()
SteeringCommitteeDisplaySchema['title'].widget.description = _(u'The title of this steering committee display.')
SteeringCommitteeDisplaySchema['description'].storage = atapi.AnnotationStorage()
SteeringCommitteeDisplaySchema['description'].widget.description = _(u'A short summary of this steering committee display.')
finalizeATCTSchema(SteeringCommitteeDisplaySchema, folderish=False, moveDiscussion=False)

class SteeringCommitteeDisplay(base.ATCTContent):
    '''Steering committee display.'''
    implements(ISteeringCommitteeDisplay)
    portal_type               = 'Steering Committee Display'
    _at_rename_after_creation = True
    schema                    = SteeringCommitteeDisplaySchema
    title                     = atapi.ATFieldProperty('title')
    description               = atapi.ATFieldProperty('description')

atapi.registerType(SteeringCommitteeDisplay, PROJECTNAME)
