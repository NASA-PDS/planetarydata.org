# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
IPDA Site Project Management: interfaces
'''

from zope.interface import Interface
from zope import schema
from zope.container.constraints import contains
from ipdasite.projectmgmt import IPDAMessageFactory as _
from Products.ATContentTypes.interface import IATEvent, IATDocument, IATFolder, IATFile
from Products.ATContentTypes.interface.image import IImageContent

class IIPDAHome(IATDocument):
    '''IPDA Home Page'''
    # no additional attributes necessary
    

class IIPDAEvent(IATEvent, IImageContent):
    '''IPDA Event'''
    # imageCaption = schema.TextLine(title=_(u'Caption'), description=_(u'Caption describing the image.'))
    

class IProjectFolder(IATFolder):
    '''Project Folder.'''
    contains('ipdasite.projectmgmt.IIPDAProject')
    # no other attributes


class IIPDAProject(IATFolder):
    '''IPDA Project.'''
    code = schema.TextLine(
        title=_(u'Code'),
        description=_(u'Three-letter code identifying this project.'),
        min_length=3,
        max_length=3,
        required=True
    )
    chairPerson = schema.TextLine(
        title=_(u'Chair Person'),
        description=_(u'User name of the chair person of this project.'),
        min_length=1,
        required=True
    )
    active = schema.Bool(
        title=_(u'Active'),
        description=_(u'True if this project is active, false otherwise.'),
        required=False,
    )
    

class IIPDAContent(Interface):
    '''Generic IPDA content adds a disgustingly awful "document ID".'''
    documentID = schema.TextLine(
        title=_(u'IPDA Document ID'),
        description=_(u'Enter the IPDA document ID including working group (WKG), document type (DT), number (NNN), version (V), revision (R), date (YYYYMMMDD) and name (NAME). Use the "Title" field to give a more readable name.'),
        required=True,
        min_length=31,
        default=u'IPDA-WKG-DT-NNN_V_R_YYYYMMMDD-NAME'
    )
    
class IIPDADocument(IIPDAContent, IATDocument):
    '''An IPDA document is like a plain document but also has a document ID.'''
    
class IIPDAFile(IIPDAContent, IATFile):
    '''An IPDA file is like a plain file but also has a document ID.'''
    
class ISteeringCommitteeDisplay(Interface):
    '''A display of the IPDA steering committee with a search and some text.'''
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'The title of this steering committee display.'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of this steering committee display.'),
        required=False,
    )
