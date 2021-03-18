# encoding: utf-8
# Copyright 2010 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''IPDA Service Registry: browser views.
'''

from Acquisition import aq_inner
from ipdasite.services.config import ADD_PERMISSIONS
from ipdasite.services.interfaces import ICurator, IService
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api

class ServiceRegistryView(BrowserView):
    '''Default view for a Service Registry.'''
    __call__ = ViewPageTemplateFile('templates/serviceregistry.pt')
    def haveServices(self):
        return len(self.services()) > 0
    def haveCurators(self):
        return len(self.curators()) > 0
    @memoize
    def curators(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        curatorBrains = catalog(
            object_provides=ICurator.__identifier__,
            path=dict(query='/'.join(context.getPhysicalPath()), depth=1),
            sort_on='sortable_title'
        )
        return [dict(title=i.Title, description=i.Description, url=i.getURL()) for i in curatorBrains]
    @memoize
    def services(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        serviceBrains = catalog(
            object_provides=IService.__identifier__,
            path=dict(query='/'.join(context.getPhysicalPath()), depth=1),
            sort_on='sortable_title'
        )
        services = []
        for serviceBrain in serviceBrains:
            services.append(dict(
                title=serviceBrain.Title,
                description=serviceBrain.Description,
                versionID=serviceBrain.versionID,
                url=serviceBrain.getURL(),
            ))
        return services
    @memoize
    def submitServiceURL(self):
        context = aq_inner(self.context)
        propsTool = getToolByName(context, 'portal_properties')
        siteProps = propsTool.site_properties
        submitURL = siteProps.getProperty('ipdaToolSubmissionURL')
        if submitURL: return submitURL
        return api.portal.get().absolute_url() + u'/services/submit-a-new-tool'
    @memoize
    def addServiceURL(self):
        context = aq_inner(self.context)
        return context.absolute_url() + '/createObject?type_name=Service'
    @memoize
    def addCuratorURL(self):
        context = aq_inner(self.context)
        return context.absolute_url() + '/createObject?type_name=Curator'
    @memoize
    def showAddServiceButton(self):
        context = aq_inner(self.context)
        portalMembership = getToolByName(context, 'portal_membership')
        return portalMembership.checkPermission(ADD_PERMISSIONS['Service'], context)
    @memoize
    def showAddCuratorButton(self):
        context = aq_inner(self.context)
        portalMembership = getToolByName(context, 'portal_membership')
        return portalMembership.checkPermission(ADD_PERMISSIONS['Curator'], context)

class ServiceView(BrowserView):
    '''Default view for a Service.'''
    __call__ = ViewPageTemplateFile('templates/service.pt')
    def haveBindings(self):
        return len(self.bindings()) > 0
    @memoize
    def bindings(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(path=dict(query='/'.join(context.getPhysicalPath()), depth=1), sort_on='sortable_title')
        return [dict(title=i.Title, description=i.Description, versionID=i.versionID, url=i.getURL()) for i in results]
    @memoize
    def addBindingURL(self):
        context = aq_inner(self.context)
        return context.absolute_url() + '/createObject?type_name=Service+Binding'
    @memoize
    def showAddBindingButton(self):
        context = aq_inner(self.context)
        portalMembership = getToolByName(context, 'portal_membership')
        return portalMembership.checkPermission(ADD_PERMISSIONS['Service Binding'], context)

class ServiceBindingView(BrowserView):
    '''Default view for a Service Binding.'''
    __call__ = ViewPageTemplateFile('templates/servicebinding.pt')
    def haveSpecifications(self):
        return len(self.specifications()) > 0
    @memoize
    def specifications(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        results = catalog(path=dict(query='/'.join(context.getPhysicalPath()), depth=1), sort_on='sortable_title')
        return [dict(title=i.Title, description=i.Description, versionID=i.versionID, url=i.getURL()) for i in results]
    @memoize
    def addSpecificationURL(self):
        context = aq_inner(self.context)
        return context.absolute_url() + '/createObject?type_name=Specification+Link'
    @memoize
    def showAddSpecificationButton(self):
        context = aq_inner(self.context)
        portalMembership = getToolByName(context, 'portal_membership')
        return portalMembership.checkPermission(ADD_PERMISSIONS['Specification Link'], context)
    

class SpecificationLinkView(BrowserView):
    '''Default view for a SpecificationLink.'''
    __call__ = ViewPageTemplateFile('templates/specificationlink.pt')
    def haveSpecificationObject(self):
        context = aq_inner(self.context)
        return context.specificationObject is not None
    

class CuratorView(BrowserView):
    '''Default view for a Curator.'''
    __call__ = ViewPageTemplateFile('templates/curator.pt')
    

