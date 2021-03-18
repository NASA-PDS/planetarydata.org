# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from curator import ICurator
from ipdasite.services import ProjectMessageFactory as _
from registryobject import IRegistryObject
from zope import schema
from zope.container.constraints import contains

class IService(IRegistryObject):
    '''A service provides a use to externals software.'''
    contains('ipdasite.services.interfaces.IServiceBinding')
    # Additional "slots" for IPDA:
    toolURL = schema.TextLine(
        title=_(u'Tool URL'),
        description=_(u'URL to the tool described by this "service".'),
        required=False,
    )
    releaseDate = schema.Datetime(
        title=_(u'Release Date'),
        description=_(u'Date of latest release.'),
        required=False,
    )
    categories = schema.Choice(
        title=_(u'Category'),
        description=_(u'One or more terms used to group tools.'),
        required=False,
        vocabulary=u'ipdasite.services.ServiceCategories',
    )
    interfaceTypes = schema.Choice(
        title=_(u'Interface Types'),
        description=_(u'Types of interface presented by the service and/or tool.'),
        required=False,
        vocabulary=u'ipdasite.services.InterfaceTypes',
    )
    abstract = schema.Text(
        title=_(u'Abstract'),
        description=_(u'A longer summary than a mere description that tells a lot more about the service, but not too long.'),
        required=False,
    )
    operatingSystems = schema.Choice(
        title=_(u'Operating Systems'),
        description=_(u'Computer platforms on which the service is available, if applicable'),
        required=False,
        vocabulary=u'ipdasite.services.OperatingSystems',
    )
    requirements = schema.Text(
        title=_(u'Requirements'),
        description=_(u'Any special pre-requisites that must be met before using this service.'),
        required=False,
    )
    curator = schema.Object(
        title=_(u'Curator'),
        description=_(u'Agency responsible for this service.'),
        required=False,
        schema=ICurator
    )
