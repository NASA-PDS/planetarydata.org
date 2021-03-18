# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from zope.component import getUtility
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from Products.CMFCore.utils import getToolByName

_ipda_theme = u'IPDA Theme'
_old_viewlet = u'ipda.topmost'
_old_css_id = '++resource++ipdasite.theme.stylesheets/main.css'
_ipda_selections = (
    'custom',
    'PloneFormGen',
    'tinymce',
    'referencebrowser',
    'ipdasite_theme_custom_images',
    'ipdasite_theme_custom_templates',
    'CMFPlacefulWorkflow',
    'LanguageTool',
    'cmfeditions_views',
    'CMFEditions',
    'kupu_tests',
    'PasswordReset',
    'ATContentTypes',
    'archetypes',
    'mimetypes_icons',
    'plone_ecmascript',
    'plone_wysiwyg',
    'plone_prefs',
    'plone_templates',
    'classic_styles',
    'plone_form_scripts',
    'plone_scripts',
    'plone_forms',
    'plone_images',
    'plone_content',
    'plone_login',
    'plone_deprecated',
    'plone_3rdParty',
    'cmf_legacy',
    'plone_kss',
    'archetypes_kss',
)
_javascripts = (
    'jquery.js',
    'jquery-integration.js',
    '++resource++plone.app.jquerytools.js',
    '++resource++plone.app.jquerytools.validator.js',
    '++resource++plone.app.jquerytools.rangeinput.js',
    '++resource++plone.app.jquerytools.dateinput.js',
    '++resource++plone.app.jquerytools.plugins.js',
    '++resource++plone.app.jquerytools.overlayhelpers.js',
    '++resource++plone.app.jquerytools.form.js',
    'event-registration.js',
    'register_function.js',
    'plone_javascript_variables.js',
    'nodeutilities.js',
    'cookie_functions.js',
    'livesearch.js',
    'fullscreenmode.js',
    'select_all.js',
    'dragdropreorder.js',
    'mark_special_links.js',
    'collapsiblesections.js',
    'form_tabbing.js',
    'popupforms.js',
    'input-label.js',
    'jquery.highlightsearchterms.js',
    'first_input_focus.js',
    'accessibility.js',
    'styleswitcher.js',
    'toc.js',
    'collapsibleformfields.js',
    '++resource++plone.app.discussion.javascripts/comments.js',
    'sarissa.js',
    'dropdown.js',
    'table_sorter.js',
    'calendar_formfield.js',
    'formUnload.js',
    'formsubmithelpers.js',
    'unlockOnFormUnload.js',
    'tiny_mce.js',
    '++resource++MochiKit.js',
    '++resource++prototype.js',
    '++resource++effects.js',
    '++resource++cssQuery-compat.js',
    '++resource++base2-dom-fp.js',
    '++resource++kukit.js',
    '++resource++kukit-devel.js',
    'tiny_mce_init.js',
    'iefixes.js',
)
_obsoleteJavascripts = (
    'se-highlight.js',
    'ie5fixes.js',
    'iefixes.js',
)
# ID, enabled, compression
_newJavascripts = (
    ('++resource++plone.app.jquerytools.validator.js', False, 'none'),
    ('++resource++plone.app.jquerytools.rangeinput.js', False, 'none'),
    ('++resource++plone.app.jquerytools.dateinput.js', False, 'none'),
    ('++resource++plone.app.discussion.javascripts/comments.js', True, 'safe'),
)
_disabledJavascripts = (
    'event-registration.js',
    'mark_special_links.js',
    '++resource++kukit-devel.js',
)
_enabledJavascripts = (
    'popupforms.js',
)

def upgradeNGTheme(setupTool):
    setupTool.runImportStepFromProfile('profile-ipdasite.theme:default', 'viewlets')
    return
    '''Upgrade to the next-generation (Diazo) IPDA theme.'''
    # Remove the old stylesheet
    css = getToolByName(setupTool, 'portal_css')
    if _old_css_id in css.getResourceIds():
        css.unregisterResource(_old_css_id)
    # Remove old skin layers
    skins = getToolByName(setupTool, 'portal_skins')
    for i in ('ipdasite_theme_custom_images', 'ipdasite_theme_styles'):
        if i in skins.objectIds():
            skins.manage_delObjects(i)
    # Make sure our skin is still selected and active
    if skins.getDefaultSkin() != _ipda_theme:
        skins.manage_properties(default_skin=_ipda_theme)
    skins.selections[_ipda_theme] = ','.join(_ipda_selections)
    if _ipda_theme in skins.selections:
        # del skins.selections[_old_theme]
        pass
    if 'main_template' in skins.custom.keys():
        skins.custom.manage_delObjects('main_template')
    # Nuke the old viewlets.  (Why is there no "public" interface to do this?)
    storage = getUtility(IViewletSettingsStorage)
    for d in (storage._order, storage._hidden):
        if _ipda_theme in d:
            del d[_ipda_theme]
    if _old_viewlet in storage._defaults:
        del storage._defaults[_old_viewlet]
    # Fix the Javascripts
    javascripts = getToolByName(setupTool, 'portal_javascripts')
    for jsID, enabled, compression in _newJavascripts:
        javascripts.registerScript(jsID, '', False, enabled, True, compression, True, '', False)
    for jsID in _enabledJavascripts:
        javascripts.getResource(jsID).setEnabled(True)
    for jsID in _disabledJavascripts:
        javascripts.getResource(jsID).setEnabled(False)
    for jsID in _obsoleteJavascripts:
        javascripts.unregisterResource(jsID)
    # FIx compression of this one guy
    resource = javascripts.getResource('++resource++plone.app.jquerytools.form.js')
    resource.setCompression('none')
    for jsID in _javascripts:
        javascripts.moveResourceToBottom(jsID)
    javascripts.cookResources()


def nullStep(setupTool, logger=None):
    pass
