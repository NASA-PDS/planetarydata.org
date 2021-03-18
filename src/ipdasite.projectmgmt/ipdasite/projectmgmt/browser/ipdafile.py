# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.
'''
IPDA Site Project Management: view for the IPDA home page
'''

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class IPDAFileView(BrowserView):
    '''Default view for an IPDA file.'''
    __call__ = ViewPageTemplateFile('templates/ipdafile.pt')
