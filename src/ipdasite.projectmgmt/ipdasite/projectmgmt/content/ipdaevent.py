# encoding: utf-8
# Copyright 2008 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
IPDA Site Project Management: IPDA Event
'''

from ipdasite.projectmgmt import IPDAMessageFactory as _
from ipdasite.projectmgmt.config import PROJECTNAME
from ipdasite.projectmgmt.interfaces import IIPDAEvent
from Products.Archetypes import atapi
from Products.ATContentTypes.content import event
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from zope.interface import implements
from Products.ATContentTypes.configuration import zconf
from Products.validation import V_REQUIRED

IPDAEventSchema = event.ATEventSchema.copy() + atapi.Schema((
    atapi.ImageField(
        'image',
        required=False,
        storage=atapi.AnnotationStorage(migrate=True),
        languageIndependent=True,
        max_size=zconf.ATNewsItem.max_image_dimension,
        sizes={
            'large'   : (768, 768),
            'preview' : (400, 400),
            'mini'    : (200, 200),
            'thumb'   : (128, 128),
            'tile'    :  (64, 64),
            'icon'    :  (32, 32),
            'listing' :  (16, 16),
        },
        validators=(('isNonEmptyFile', V_REQUIRED), ('checkNewsImageMaxSize', V_REQUIRED)),
        widget=atapi.ImageWidget(
            description=_(u'An image for this event, such as a photograph of the venue.'),
            label=_(u'Image'),
            show_content_type=False,
        )
    ),
    atapi.StringField(
        'imageCaption',
        required=False,
        searchable=True,
        widget=atapi.StringWidget(
            description=_(u'An optional caption for the image.'),
            label=_(u'Image Caption'),
            size=40,
        ),
    ),
))
finalizeATCTSchema(IPDAEventSchema, folderish=False, moveDiscussion=True)
# finalizeATCTSchema moves 'location' into 'categories', we move it back:
IPDAEventSchema.changeSchemataForField('location', 'default')
IPDAEventSchema.moveField('location', before='startDate')

class IPDAEvent(event.ATEvent):
    '''An IPDA Event.'''
    implements(IIPDAEvent)
    portal_type               = 'IPDA Event'
    _at_rename_after_creation = True
    schema                    = IPDAEventSchema
    def tag(self, **kwargs):
        """Generate image tag using the api of the ImageField
        """
        return self.getField('image').tag(self, **kwargs)
    def __bobo_traverse__(self, REQUEST, name):
        """Give transparent access to image scales. This hooks into the
        low-level traversal machinery, checking to see if we are trying to
        traverse to /path/to/object/image_<scalename>, and if so, returns
        the appropriate image content.
        """
        if name.startswith('image'):
            field = self.getField('image')
            image = None
            if name == 'image':
                image = field.getScale(self)
            else:
                scalename = name[len('image_'):]
                if scalename in field.getAvailableSizes(self):
                    image = field.getScale(self, scale=scalename)
            if image is not None and not isinstance(image, basestring):
                # image might be None or '' for empty images
                return image
        return super(IPDAEvent, self).__bobo_traverse__(REQUEST, name)
    
    


atapi.registerType(IPDAEvent, PROJECTNAME)