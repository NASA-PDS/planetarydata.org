# encoding: utf-8
# Copyright 2008 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
IPDA Site Project Management: IPDA Project
'''

from ipdasite.projectmgmt import IPDAMessageFactory as _
from ipdasite.projectmgmt.config import PROJECTNAME
from ipdasite.projectmgmt.interfaces import IIPDAProject
from Products.Archetypes import atapi
from plone.app.folder import folder
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from zope.interface import implements
from Products.validation.config import validation
from Products.validation.validators import RegexValidator

class CodeValidator(RegexValidator):
    def __init__(self, name, title, description):
        RegexValidator.__init__(self, name, r'^[A-Za-z]{3}$', title=title, description=description,
            errmsg=_(u'Is not a valid 3-letter code'))
validation.register(CodeValidator('isValidCode', _(u'Project Code Validator'), _(u'Checks if we have a 3-letter code.')))

IPDAProjectSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    atapi.StringField(
        'code',
        required=True,
        validators=('isValidCode',),
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'Code'),
            description=_(u'Three-letter code identifying this project.'),
        ),
    ),
    atapi.StringField(
        'chairPerson',
        required=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'Chair Person'),
            description=_(u'User name of the chair person of this project.'),
        ),
    ),
    atapi.BooleanField(
        'active',
        required=False,
        storage=atapi.AnnotationStorage(),
        widget=atapi.BooleanWidget(
            label=_(u'Active'),
            description=_(u'True if this project is active, false otherwise.'),
        ),
    ),
))
IPDAProjectSchema['title'].storage = atapi.AnnotationStorage()
IPDAProjectSchema['description'].storage = atapi.AnnotationStorage()
finalizeATCTSchema(IPDAProjectSchema, folderish=True, moveDiscussion=True)

class IPDAProject(folder.ATFolder):
    '''IPDA Project.'''
    implements(IIPDAProject)
    portal_type               = 'IPDA Project'
    _at_rename_after_creation = True
    schema                    = IPDAProjectSchema
    title                     = atapi.ATFieldProperty('title')
    description               = atapi.ATFieldProperty('description')
    code                      = atapi.ATFieldProperty('code')
    chairPerson               = atapi.ATFieldProperty('chairPerson')
    active                    = atapi.ATFieldProperty('active')

atapi.registerType(IPDAProject, PROJECTNAME)
