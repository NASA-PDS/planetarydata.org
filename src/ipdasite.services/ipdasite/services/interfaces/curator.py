# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Curator: interface'''

from zope.interface import Interface
from zope import schema
from ipdasite.services import ProjectMessageFactory as _

class ICurator(Interface):
    '''A person and agency that is responsible for a service.'''
    title = schema.TextLine(
        title=_(u'Name'),
        description=_(u'Name of this curator.'),
        required=True,
    )
    description = schema.Text(
        title=_(u'Description'),
        description=_(u'A short summary of this curator, used in free-text searches.'),
        required=False,
    )
    contactName = schema.TextLine(
        title=_(u'Contact Name'),
        description=_(u'Name of a person who curates one or more services.'),
        required=False,
    )
    emailAddress = schema.TextLine(
        title=_(u'Email Address'),
        description=_(u'Contact address for a person or workgroup that curates services.'),
        required=False,
    )
    telephone = schema.TextLine(
        title=_(u'Telephone'),
        description=_(u'Public telephone number in international format in order to contact this curator.'),
        required=False,
    )
