# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from identifiable import IIdentifiable
from zope import schema
from ipdasite.services import ProjectMessageFactory as _

class IRegistryObject(IIdentifiable):
    '''A registry object in the ebXML registry sense.'''
    title = schema.TextLine(
        title=_(u'Name'),
        description=_(u'Name of this service'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of this service.'),
        required=False,
    )
    lid = schema.TextLine(
        title=_(u'LID'),
        description=_(u'Logical Identifier'),
        required=True,
    )
    versionID = schema.TextLine(
        title=_(u'Version ID'),
        description=_(u'The version of this service (as chosen by the service registrant).'),
        required=True,
        default=u'0.0.0',
    )
