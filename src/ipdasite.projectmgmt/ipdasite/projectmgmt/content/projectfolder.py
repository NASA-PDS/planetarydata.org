# encoding: utf-8
# Copyright 2008 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
IPDA Site Project Management: Project Folder
'''

from ipdasite.projectmgmt.config import PROJECTNAME
from ipdasite.projectmgmt.interfaces import IProjectFolder
from Products.Archetypes import atapi
from plone.app.folder import folder
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from zope.interface import implements

ProjectFolderSchema = folder.ATFolderSchema.copy() + atapi.Schema((
    # No other attributes.
))
ProjectFolderSchema['title'].storage = atapi.AnnotationStorage()
ProjectFolderSchema['description'].storage = atapi.AnnotationStorage()
finalizeATCTSchema(ProjectFolderSchema, folderish=True, moveDiscussion=True)

class ProjectFolder(folder.ATFolder):
    '''Project folder.'''
    implements(IProjectFolder)
    portal_type               = 'Project Folder'
    _at_rename_after_creation = True
    schema                    = ProjectFolderSchema
    title                     = atapi.ATFieldProperty('title')
    description               = atapi.ATFieldProperty('description')
    

atapi.registerType(ProjectFolder, PROJECTNAME)
