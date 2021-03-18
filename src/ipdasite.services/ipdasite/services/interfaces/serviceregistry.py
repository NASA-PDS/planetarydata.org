 # encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from ipdasite.services import ProjectMessageFactory as _
from zope import schema
from zope.container.constraints import contains
from zope.interface import Interface

class IServiceRegistry(Interface):
    '''A registry that contains definitions of services.'''
    contains('ipdasite.services.interfaces.IService')
    title = schema.TextLine(
        title=_(u'Title'),
        description=_(u'The name of this service registry.'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of this service registry.'),
        required=False,
    )
    home = schema.URI(
        title=_(u'Home'),
        description=_(u'Base URI of the registry.'),
        required=True,
    )
    sync = schema.Bool(
        title=_(u'Synchronize'),
        description=_(u'Enable synchronization with a PDS Registry Service at the home URL.'),
        required=False,
    )
    