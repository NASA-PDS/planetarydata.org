# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from ipdasite.services import ProjectMessageFactory as _
from registryobject import IRegistryObject
from zope import schema
from zope.container.constraints import contains

class IServiceBinding(IRegistryObject):
    '''A service binding identifies the endpoint and specifications for a service.'''
    contains('ipdasite.services.interfaces.ISpecificationLink')
    accessURI = schema.TextLine(
        title=_(u'Access URI'),
        description=_(u'URI that identifies the endpoint where the service may be accessed.'),
        required=False,
    )
    