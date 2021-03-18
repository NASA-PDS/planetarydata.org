IPDA Site Views
===============

This module, ``ipdasite.views``, provides a custom, tabular view for folders
that was requested by Emily Law.  This enables folders in the International
Planetary Data Website, hosted at http://planetarydata.org/, and powered by
Plone_, to display a table of folder contents that, for some reason, is
desirable by some.


The Tabular View
================

This package's view is the IPDA Tabular View.  To demonstrate it, we'll start up a Plone site and use a test browser to navigate
it, create a folder, add some content, and then try out the view.  First,
let's set up the site::

    >>> app = layer['app']
    >>> from plone.testing.z2 import Browser
    >>> from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
    >>> browser = Browser(app)
    >>> browser.handleErrors = False
    >>> browser.addHeader('Authorization', 'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
    >>> portal = layer['portal']    
    >>> portalURL = portal.absolute_url()

And now let's make a folder::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='folder').click()
    >>> browser.getControl(name='title').value = u"Emily's Law"
    >>> browser.getControl(name='description').value = u'This folder demonstrates the view.'
    >>> browser.getControl(name='form.button.save').click()

Now we'll add a couple of items::

    >>> browser.open(portalURL + '/emilys-law')
    >>> browser.getLink(id='document').click()
    >>> browser.getControl(name='title').value = u"Why I Like Tables"
    >>> browser.getControl(name='description').value = u'A treatise on the beauty of rectangular data.'
    >>> browser.getControl(name='text').value = u'<p>I love <em>tables</em>!</p>'
    >>> browser.getControl(name='form.button.save').click()

    >>> browser.open(portalURL + '/emilys-law')
    >>> browser.getLink(id='document').click()
    >>> browser.getControl(name='title').value = u"Other Kinds of Tables"
    >>> browser.getControl(name='description').value = u'An examination of other tables, like furniture.'
    >>> browser.getControl(name='text').value = u'<p>There are many kinds of tables.</p>'
    >>> browser.getControl(name='form.button.save').click()

Now, let's visit the folder and change the view::

    >>> browser.open(portalURL + '/emilys-law')
    >>> l = browser.getLink(id='plone-contentmenu-display-IPDA-tabular-view')
    >>> l.text
    'IPDA-tabular-view'
    >>> l.click()
    >>> browser.contents
    '...Title...Version...Status...Release Date...Contact...'
    >>> browser.contents
    '...Why I Like Tables...N/A...N/A...N/A...admin...Other Kinds of Tables...N/A...N/A...N/A...admin...'

Yeeesh.  But that's what she wanted.

That's it.

.. References:
.. _Plone: http://plone.org/

