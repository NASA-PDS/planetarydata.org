# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from ipdasite.services import ProjectMessageFactory as _
from registryobject import IRegistryObject
from zope import schema
from zope.interface import Interface

class ISpecificationLink(IRegistryObject):
    '''Provides the linkage between a Service Binding and its technical specification.'''
    specificationObject = schema.Object(
        title=_(u'Specification Object'),
        description=_(u'Object that provides the technical specification for a service binding.'),
        required=False,
        schema=Interface
    )
    usageDescription = schema.Text(
        title=_(u'Usage Description'),
        description=_(u'Tells how to use the optional usage parameters'),
        required=False,
    )
    usageParameters = schema.List(
        title=_(u'Usage Parameters'),
        description=_(u'Instance-specific parameters telling how to use the technical specification, one per line.'),
        required=False,
        value_type=schema.TextLine(
            title=_(u'Usage Parameter'),
            description=_(u'Instance-specific parameter telling how to use the technical specification.')
        )
    )
