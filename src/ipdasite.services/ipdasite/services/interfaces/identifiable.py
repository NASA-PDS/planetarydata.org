# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from zope.interface import Interface
from zope import schema
from ipdasite.services import ProjectMessageFactory as _

class IIdentifiable(Interface):
    '''An identifiable object in the ebXML registry sense.'''
    guid = schema.TextLine(
        title=_(u'GUID'),
        description=_(u'Globally Unique Identifier'),
        required=True,
    )
