# encoding: utf-8
# Copyright 2012–2014 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.
#
# Upgrade an existing installation of the IPDA site.
#
# Execute with a Zope instance's "run" command, ie:
#   bin/zope-debug run support/upgrade.py
# 
# Assumes that the instance already has a previous edition of the IPDA site installed.

_adminUser = 'admin'            # Default admin user
_adminPass = 'admin'            # Stupid default admin password
_policy    = 'ipdasite.policy'  # Name of the policy that orchestrates everything
_siteID    = 'planetarydata'    # Object ID of the PloneSite object in the Zope app server

from AccessControl.SecurityManagement import newSecurityManager, noSecurityManager
from AccessControl.SecurityManager import setSecurityPolicy
from Products.CMFCore.tests.base.security import PermissiveSecurityPolicy, OmnipotentUser
from Products.CMFCore.utils import getToolByName
from Testing import makerequest
from zope.component.hooks import setSite
import transaction, sys

app = globals().get('app') # silence pyflakes about Zope's "app" magic

def main(app, siteID, adminUser, adminPass, policy):
    try:
        # Get a test request installed.
        app = makerequest.makerequest(app)

        # Nuke all old admin users
        acl_users = app.acl_users
        admins = [i for i in acl_users.users.listUserIds()]
        for i in admins:
            acl_users.users.removeUser(i)

        # Add our new admin user
        acl_users.users.manage_addUser(adminUser, adminUser, adminPass, adminPass)

        # Set up security.
        setSecurityPolicy(PermissiveSecurityPolicy())
        newSecurityManager(None, OmnipotentUser().__of__(acl_users))

        # Get the portal.
        portal = getattr(app, siteID)
        setSite(portal)

        # Upgrade Plone
        migrationTool = getToolByName(portal, 'portal_migration')
        migrationTool.upgrade(dry_run=False)

        # Upgrade the site
        qi = getToolByName(portal, 'portal_quickinstaller')
        qi.upgradeProduct(_policy)

        # Commit everything and shut down.
        transaction.commit()
        noSecurityManager()
    except Exception, ex:
        print ex
        return False
    return True

if __name__ == '__main__':
    adminUser = _adminUser if len(sys.argv) < 4 else sys.argv[3]
    adminPass = _adminPass if len(sys.argv) < 5 else sys.argv[4]
    rc = main(app, _siteID, adminUser, adminPass, _policy)
    sys.exit(0 if rc else -1)
