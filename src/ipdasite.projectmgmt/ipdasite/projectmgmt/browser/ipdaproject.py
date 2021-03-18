# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.
'''
IPDA Site Project Management: view for an IPDA Project
'''

from Acquisition import aq_inner
from ipdasite.projectmgmt.interfaces import IIPDAProject
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class IPDAProjectView(BrowserView):
    '''Default view for a project folder.'''
    __call__ = ViewPageTemplateFile('templates/ipdaproject.pt')
