# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Curator: implementation'''

from ipdasite.services import ProjectMessageFactory as _
from ipdasite.services.config import PROJECTNAME
from ipdasite.services.interfaces import ICurator
from Products.Archetypes import atapi
from Products.ATContentTypes.content import base, schemata
from Products.CMFCore.utils import getToolByName
from zope.interface import implements, directlyProvides
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary

CuratorSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema((
    atapi.StringField(
        'contactName',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u'Contact Name'),
            description=_(u'Name of a person who curates one or more services.'),
        ),
    ),
    atapi.StringField(
        'emailAddress',
        required=False,
        searchable=False,
        storage=atapi.AnnotationStorage(),
        validators=('isEmail',),
        widget=atapi.StringWidget(
            label=_(u'Email Address'),
            description=_(u'Contact address for a person or workgroup that curates services.'),
        ),
    ),
    atapi.StringField(
        'telephone',
        required=False,
        searchable=False,
        storage=atapi.AnnotationStorage(),
        validators=('isInternationalPhoneNumber',),
        widget=atapi.StringWidget(
            label=_(u'Telephone'),
            description=_(u'Public telephone number in international format in order to contact this curator.'),
        ),
    ),
))

CuratorSchema['title'].storage = atapi.AnnotationStorage()
CuratorSchema['title'].widget.label=_(u'Name')
CuratorSchema['title'].widget.description=_(u'Name of this curator.')
CuratorSchema['description'].storage = atapi.AnnotationStorage()
CuratorSchema['description'].widget.label=_(u'Description')
CuratorSchema['description'].widget.description=_(u'A short summary of this curator, used in free-text searches.')

schemata.finalizeATCTSchema(CuratorSchema, folderish=False, moveDiscussion=False)

class Curator(base.ATCTContent):
    '''A curator is responsible for one or more services.'''
    implements(ICurator)
    schema       = CuratorSchema
    portal_type  = 'Curator'
    contactName  = atapi.ATFieldProperty('contactName')
    description  = atapi.ATFieldProperty('description')
    emailAddress = atapi.ATFieldProperty('emailAddress')
    telephone    = atapi.ATFieldProperty('telephone')
    title        = atapi.ATFieldProperty('title')

atapi.registerType(Curator, PROJECTNAME)

def CuratorsVocabulary(context):
    catalog = getToolByName(context, 'portal_catalog')
    results = catalog(object_provides=ICurator.__identifier__, sort_on='sortable_title')
    items = [(i.Title, i.UID) for i in results]
    return SimpleVocabulary.fromItems(items)
directlyProvides(CuratorsVocabulary, IVocabularyFactory)
