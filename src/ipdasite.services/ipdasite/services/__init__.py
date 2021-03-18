# encoding: utf-8
# Copyright 2011–2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''IPDA Service Registry.'''

from zope.i18nmessageid import MessageFactory
from ipdasite.services import config
from Products.Archetypes import atapi
import Products.CMFCore

ProjectMessageFactory = MessageFactory(config.PROJECTNAME)

def initialize(context):
    '''Initializer called when used as a Zope 2 product.'''
    from content import serviceregistry, service, servicebinding, specificationlink, curator # for lame side effect
    contentTypes, constructors, ftis = atapi.process_types(atapi.listTypes(config.PROJECTNAME), config.PROJECTNAME)
    for atype, constructor in zip(contentTypes, constructors):
        Products.CMFCore.utils.ContentInit(
            '%s: %s' % (config.PROJECTNAME, atype.portal_type),
            content_types=(atype,),
            permission=config.ADD_PERMISSIONS[atype.portal_type],
            extra_constructors=(constructor,)
        ).initialize(context)
