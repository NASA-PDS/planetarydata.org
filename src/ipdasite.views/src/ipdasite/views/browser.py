# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from Acquisition import aq_inner
from five import grok
from Products.ATContentTypes.interfaces import IATFolder
from plone.memoize.view import memoize
from Products.CMFCore.utils import getToolByName

class IPDATabularView(grok.View):
    '''Customized tabular view for folders requested by Emily Law.'''
    grok.context(IATFolder)
    grok.require('zope2.View')
    grok.name('IPDA-tabular-view')
    def update(self):
        super(IPDATabularView, self).update()
    def folderContents(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        return catalog(path=dict(query='/'.join(context.getPhysicalPath()), depth=1), sort_on='sortable_title')
        
        