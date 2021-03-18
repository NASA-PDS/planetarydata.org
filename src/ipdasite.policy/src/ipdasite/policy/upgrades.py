# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from plone.contentrules.engine.interfaces import IRuleStorage
from plone.portlets.interfaces import IPortletManager, IPortletAssignmentMapping
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
from zope.component import getUtility, getMultiAdapter
import transaction

_profileID = 'profile-ipdasite.policy:default'

_ipdaHomeDescription = u'''Welcome to the International Planetary Data Alliance.'''
_ipdaHomeBody = u'''<h2 class="callout" style="text-align: center; ">
    <img class="image-inline" src="Members/kelly/generic-ipda-splash" alt='Discover more with the IPDA'/>
</h2>
<p>The IPDA's main emphasis is to ease discovery, access and use of planetary data by world-wide scientists regardless of which agency is collecting and distributing the data. Ensuring proper capture, accessibility and availability of the data is the task of the individual space agencies. The IPDA is focusing on developing an international standard which allows the following capabilities: query, access and usage of data across international planetary data archive systems. While, trends in other areas of space science are concentrating on the sharing of science data from diverse standards and collection methods, the IPDA shall concentrate on promoting standards which drive common methods for collecting and describing planetary science data across the international community. Such an approach will better support the long term goal of easing data sharing across system and agency boundaries. An initial starting point for developing such a standard will be internationalization of NASA's Planetary Data System standards.</p>
<p> </p>
<p>Feel free to explore this site and check out the latest status in our <a class="internal-link" href="documents/newsletters">newsletters</a>.</p>'''

def _getPortal(setupTool):
    '''Get the portal that the setup tool is servicing.'''
    return getToolByName(setupTool, 'portal_url').getPortalObject()

def _doPublish(item, workflowTool, action='publish'):
    try:
        workflowTool.doActionFor(item, action=action)
        item.reindexObject()
    except WorkflowException:
        pass
    if IFolderish.providedBy(item):
        for childID, childItem in item.contentItems():
            _doPublish(childItem, workflowTool, action)


def nullUpgradeStep(setupTool):
    '''A no-op step for when no custom upgrade is necessary.'''
    return

class DisabledLinkRules(object):
    def __init__(self, portal):
        self.portal = portal
        self.propTool = getToolByName(portal, 'portal_properties')
        self.origLinkIntegrityMode = self.propTool.site_properties.getProperty('enable_link_integrity_checks', True)
        self.contentRuleStorage = getUtility(IRuleStorage)
        self.origContentRuleMode = self.contentRuleStorage.active
    def __enter__(self):
        self.propTool.manage_changeProperties(enable_link_integrity_checks=False)
        self.contentRuleStorage.active = False
        return self.portal
    def __exit__(self, type, value, traceback):
        self.propTool.manage_changeProperties(enable_link_integrity_checks=self.origLinkIntegrityMode)
        self.contentRuleStorage.active = self.origContentRuleMode
        transaction.commit()

def fixTEG(setupTool):
    '''Fix the Technical Experts Group.'''
    portal = _getPortal(setupTool)
    with DisabledLinkRules(portal):
        documents = portal['documents']
        if 'technical-experts-group' not in documents.keys():
            # No TEG?  Nothing to do.
            return
        teg = documents['technical-experts-group']
        if teg.portal_type == 'Folder':
            # Already fixed?  Nothing to do.
            return
        documents.manage_renameObject('technical-experts-group', 'technical-experts-group-orig')
        oldTEG = documents['technical-experts-group-orig']
        teg = documents[documents.invokeFactory('Folder', 'technical-experts-group')]
        teg.setTitle(u'Technical Experts Group')
        teg.setDescription(u'This is the wiki (collaborative workspace) for the Technical Experts Group (TEG) of the Interplanetary Data Alliance (IPDA).')
        teg.reindexObject()
        itemsToMove = [itemID for itemID, item in oldTEG.contentItems()]
        teg.manage_pasteObjects(oldTEG.manage_cutObjects(itemsToMove))
        workflowTool = getToolByName(portal, 'portal_workflow')
        _doPublish(teg, workflowTool)
        documents.manage_delObjects('technical-experts-group-orig')
    qi = getToolByName(portal, 'portal_quickinstaller')
    qi.uninstallProducts(['borg.project'])

def recreateHome(setupTool):
    '''Redo the home page'''
    portal = _getPortal(setupTool)
    if 'welcome-to-the-ipda' not in portal.keys():
        return
    currentHome = portal['welcome-to-the-ipda']
    if currentHome.portal_type == 'Document':
        return
    portal.manage_delObjects('welcome-to-the-ipda')
    home = portal[portal.invokeFactory('Document', 'welcome-to-the-ipda')]
    home.setTitle(u'Welcome to the IPDA')
    home.setDescription(_ipdaHomeDescription)
    home.setText(_ipdaHomeBody)
    home.allowDiscussion(False)
    _doPublish(home, getToolByName(portal, 'portal_workflow'))
    transaction.commit()

def upgrade34Theme(setupTool):
    setupTool.runImportStepFromProfile(_profileID, 'actions')
    portal = _getPortal(setupTool)
    qi = getToolByName(portal, 'portal_quickinstaller')
    if qi.isProductInstalled('ipdasite.theme') and int(qi.getInstallProfile('ipdasite.theme')['version']) >= 3:
        return
    # upgradeProduct isn't sufficient for the theme for some reason...
    qi.upgradeProduct('ipdasite.theme')
    # so, also reinstall it after upgrading it.  The ways of Plone are mysterious.
    qi.reinstallProducts(['ipdasite.theme'])
    transaction.commit()
    
def setupDiscussions(setupTool):
    setupTool.runImportStepFromProfile(_profileID, 'plone.app.registry')
    setupTool.runImportStepFromProfile(_profileID, 'workflow')

def setup34Views(setupTool):
    portal = _getPortal(setupTool)
    qi = getToolByName(portal, 'portal_quickinstaller')
    if qi.isProductInstalled('ipdasite.views'):
        return
    qi.installProduct('ipdasite.views')
    for i in (
        ('projects',),
        ('projects', 'active-projects-2012-2013'),
        ('projects', 'previous-projects'),
        ('projects', 'inactive-projects'),
        ('documents',),
        ('documents', 'miscellaneous'),
        ('documents', 'steering-committee'),
        ('documents', 'technical-experts-group'),
    ):
        try:
            item = portal.unrestrictedTraverse(i)
        except AttributeError:
            continue
        item.selectViewTemplate('IPDA-tabular-view')

def setup34Portlets(setupTool):
    portal = _getPortal(setupTool)
    column = getUtility(IPortletManager, name=u'plone.leftcolumn')
    manager = getMultiAdapter((portal, column), IPortletAssignmentMapping)
    order = []
    if 'search' in manager.keys():
        order.append('search')
    if 'quick-links' in manager.keys():
        order.append('quick-links')
    if 'events' in manager.keys():
        del manager['events']
    if 'news' in manager.keys():
        manager['news'].count = 3
        order.append('news')
    if 'recent-items' in manager.keys():
        order.append('recent-items')
    if 'navigation' in manager.keys():
        del manager['navigation']
    manager.updateOrder(order)

