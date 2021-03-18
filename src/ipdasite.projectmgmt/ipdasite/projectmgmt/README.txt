This package provides Plone 3 content objects that represent projects and
related artifacts that are pursued by the `International Planetary Data
Alliance`_.


Installation
============

Add ``ipdasite.projectmgmt`` to the buildout.


Content Types
=============

The content types introduced in this package include the following:

IPDA Home
    A displayable page to show introductory text, next conference, and a
    log in link for anonymous users.
IPDA Event
    Like the standard Plone event, but also includes an image.
Project Folder
    Like a standard Plone folder, but with a project identification code and a
    chair person's user name.
IPDA Document
    Like a regular document (page), but with a document ID.
IPDA File
    Like a regular file, but with a document ID.
Steering Committee Display
    A titled and described page that also includes a list of all IPDA Steering
    Committee members.

The remainder of this document demonstrates the content types using a series
of functional tests.


Tests
=====

In order to execute these tests, we'll first need a test browser::

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portalURL = self.portal.absolute_url()
        
We also change some settings so that any errors will be reported immediately::

    >>> browser.handleErrors = False
    >>> self.portal.error_log._ignored_exceptions = ()
        
We'll also turn off the portlets.  Why?  Well for these tests we'll be looking
for specific strings output in the HTML, and the portlets will often have
duplicate links that could interfere with that::

    >>> from zope.component import getUtility, getMultiAdapter
    >>> from plone.portlets.interfaces import IPortletManager, IPortletAssignmentMapping
    >>> for colName in ('left', 'right'):
    ...     col = getUtility(IPortletManager, name=u'plone.%scolumn' % colName)
    ...     assignable = getMultiAdapter((self.portal, col), IPortletAssignmentMapping)
    ...     for name in assignable.keys():
    ...         del assignable[name]

And finally we'll log in as an administrator::

    >>> from Products.PloneTestCase.setup import portal_owner, default_password
    >>> browser.open(portalURL + '/login_form?came_from=' + portalURL)
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()


Addable Content
---------------

Here we'll exercise some of the content objects available in this project and
demonstrate their properties and constraints.


IPDA Home
~~~~~~~~~

The IPDA home is essentially a custom display for the home page, although they
can be created anywhere.

    >>> browser.open(portalURL)
    >>> browser.getLink(id='ipda-home').url.endswith('createObject?type_name=IPDA+Home')
    True
    >>> browser.getLink(id='ipda-home').click()
    >>> browser.getControl(name='title').value = u'My Home'
    >>> browser.getControl(name='description').value = u'The home of IPDA.'
    >>> browser.getControl(name='text').value = u'<p>Welcome.</p>'
    >>> browser.getControl(name='form.button.save').click()
    >>> 'my-home' in portal.objectIds()
    True
    >>> myHome = portal['my-home']
    >>> myHome.title
    'My Home'
    >>> myHome.description
    'The home of IPDA.'
    >>> myHome.text
    '<p>Welcome.</p>'
    
    

IPDA Events
~~~~~~~~~~~

IPDA Events extend the ATCT Event by including an image and image caption.
Rather than exhaustively test every field, let's just set up some dates and
the image and caption. First, we'll need some image data::

    >>> import cStringIO, base64
    >>> fakeImage = cStringIO.StringIO(base64.b64decode('R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=='))
    
As well as a date for our event. Let's say tomorrow::
    
    >>> from datetime import datetime, timedelta
    >>> tomorrow = datetime.now() + timedelta(1)

Now, let's get our meeting set up.

    >>> browser.open(portalURL)
    >>> browser.getLink(id='ipda-event').click()
    >>> browser.getControl(name='title').value = u'Grand Poobah Council'
    >>> browser.getControl(name='startDate_year').displayValue = [str(tomorrow.year)]
    >>> browser.getControl(name='startDate_month').value = ['%02d' % tomorrow.month]
    >>> browser.getControl(name='startDate_day').value = ['%02d' % tomorrow.day]
    >>> dayAfter = tomorrow + timedelta(1)
    >>> browser.getControl(name='endDate_year').displayValue = [str(dayAfter.year)]
    >>> browser.getControl(name='endDate_month').value = ['%02d' % dayAfter.month]
    >>> browser.getControl(name='endDate_day').value = ['%02d' % dayAfter.day]
    >>> browser.getControl(name='image_file').add_file(fakeImage, 'image/png', 'fakeImage.png')
    >>> browser.getControl(name='imageCaption').value = u'The Poobahs love it here.'
    >>> browser.getControl(name='form.button.save').click()
    >>> 'grand-poobah-council' in portal.objectIds()
    True
    >>> event = portal['grand-poobah-council']
    >>> event.title
    u'Grand Poobah Council'
    >>> event.imageCaption
    u'The Poobahs love it here.'

Upcoming events are featured on the IPDA home page.  Let's publish this event
and see if it appears.

    >>> browser.open(portalURL + '/grand-poobah-council')
    >>> browser.getLink(id='workflow-transition-publish').click()
    >>> browser.open(portalURL + '/my-home')
    >>> browser.contents
    '...<h2>Upcoming Events</h2>...Grand Poobah Council...'    


Project Folder
~~~~~~~~~~~~~~

A project folder is like a plain folder but can hold only IPDA Projects.

    >>> browser.open(portalURL)
    >>> browser.getLink(id='project-folder').click()
    >>> browser.getControl(name='title').value = u'Black Ops'
    >>> browser.getControl(name='description').value = u'These are top-secret projects.'
    >>> browser.getControl(name='form.button.save').click()
    >>> 'black-ops' in portal.objectIds()
    True
    >>> blackOps = portal['black-ops']
    >>> blackOps.title
    'Black Ops'
    >>> blackOps.description
    'These are top-secret projects.'


IPDA Project
~~~~~~~~~~~~

Project Folders contain IPDA Projects, which can't be added anywhere else::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='ipda-project')
    Traceback (most recent call last):
    ...
    LinkNotFoundError
    >>> browser.open(portalURL + '/black-ops')
    >>> browser.getLink(id='ipda-project').click()
    >>> browser.getControl(name='title').value = u'Operation: Brown Cow'
    >>> browser.getControl(name='description').value = u'A top-secret assault on a dairy.'
    
IPDA Projects can contain anything a plain folder can.  They also have a
three-letter ID code and a chair person's user name, as well as an activity
state::

    >>> browser.getControl(name='code').value = u'XYZ'
    >>> browser.getControl(name='chairPerson').value = u'hayden'
    >>> browser.getControl('Active').selected = True
    >>> browser.getControl(name='form.button.save').click()
    >>> 'operation-brown-cow' in blackOps.objectIds()
    True
    >>> operationBrownCow = blackOps['operation-brown-cow']
    >>> operationBrownCow.title
    'Operation: Brown Cow'
    >>> operationBrownCow.description
    'A top-secret assault on a dairy.'
    >>> operationBrownCow.code
    'XYZ'
    >>> operationBrownCow.chairPerson
    'hayden'
    >>> operationBrownCow.active
    True

Let's add one more IPDA Project, but this time keep it inactive::

    >>> browser.open(portalURL + '/black-ops')
    >>> browser.getLink(id='ipda-project').click()
    >>> browser.getControl(name='title').value = u'Operation: White Cow'
    >>> browser.getControl(name='description').value = u'A top-secret assault on a vanilla farm.'
    >>> browser.getControl(name='code').value = u'ABC'
    >>> browser.getControl(name='chairPerson').value = u'dryden'
    >>> browser.getControl('Active').selected = False
    >>> browser.getControl(name='form.button.save').click()

Why? Keep reading!


Active vs Inactive Projects
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A project folder practices segregation-that is, active projects are displayed
in alphabetical order, while inactive projects are hidden in a collapsible
section.  Let's make sure that works as advertised::

    >>> browser.open(portalURL + '/black-ops')
    >>> browser.contents
    '...Active Projects...Operation: Brown Cow...Inactive Projects...Operation: White Cow...'
    
Now, if we make "Operation:  White Cow" active::

    >>> browser.open(portalURL + '/black-ops/operation-white-cow')
    >>> browser.getLink('Edit').click()
    >>> browser.getControl('Active').selected = True
    >>> browser.getControl(name='form.button.save').click()

then the Inactive Projects section should go away completely::

    >>> browser.open(portalURL + '/black-ops')
    >>> browser.contents
    '...Active Projects...Operation: Brown Cow...Operation: White Cow...'
    >>> 'Inactive Projects' in browser.contents
    False


Project Folders and Past Events
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Any past events stored anywhere in an IPDA Project get displayed up in the
Project Folder at the bottom.  I'm not sure why.  So, let's re-visit the
"Black Ops" Project Folder and ensure there are no meetings listed right now::

    >>> browser.open(portalURL + '/black-ops')
    >>> 'Meeting Archive' not in browser.contents
    True
    
Now we'll add an event set in the past inside the "Operation:  Brown Cow" IPDA
Project::

    >>> yesterday = datetime.now() - timedelta(1)
    >>> browser.open(portalURL + '/black-ops/operation-brown-cow')
    >>> browser.getLink(id='ipda-event').click()
    >>> browser.getControl(name='title').value = u'Anal Retentives Anonymous'
    >>> browser.getControl(name='startDate_year').displayValue = [str(yesterday.year)]
    >>> browser.getControl(name='startDate_month').value = ['%02d' % yesterday.month]
    >>> browser.getControl(name='startDate_day').value = ['%02d' % yesterday.day]
    >>> ending = yesterday + timedelta(hours=1)
    >>> browser.getControl(name='endDate_year').displayValue = [str(ending.year)]
    >>> browser.getControl(name='endDate_month').value = ['%02d' % ending.month]
    >>> browser.getControl(name='endDate_day').value = ['%02d' % ending.day]
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.open(portalURL + '/black-ops/operation-brown-cow/anal-retentives-anonymous')
    >>> browser.getLink(id='workflow-transition-publish').click()
    
Revisiting the project folder should now display the past meetings::

    >>> browser.open(portalURL + '/black-ops')
    >>> 'Meeting Archive' in browser.contents
    True
    >>> 'Anal Retentives Anonymous' in browser.contents
    True


Things with IPDA Document IDs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Someone involved with IPDA had an adminigasm when he or she came up with this
monstrosity::

    IPDA-DAP-TN-001_0_3_2007APR07-PLANETARY DATA ACCESS PROTOCOL
    
That's an IPDA "document ID" consisting of the following parts:

IPDA
    A prefix that indicates IPDA made this document, file, or other content.
DAP
    The three-letter project code of the project that produced the content,
    in this case, the Data Access Project.
TN
    Two-letter artifact type code. In this case, a Technical Note.
001
    Document number.  Yes, he or she expects 999 possible technical notes to
    be produced by the Data Access Project.
0
    Version number, up to 9.
3
    Release number, up to 9.
2007APR07
    Release date
PLANETARY DATA ACCESS PROTOCOL
    The actual title of the document!
    
All this annoyance is just make-work, a false of organization, and a waste of
the taxpayer money from *multiple* countries.  Now we get to test it out!

First up is an IPDA Document, which is just like a regular document but with
the document ID::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='ipda-document').url.endswith('createObject?type_name=IPDA+Document')
    True
    >>> browser.getLink(id='ipda-document').click()
    >>> browser.getControl(name='title').value = u'JZ: Secret Code or Stupid Git?'
    >>> browser.getControl(name='description').value = u'A scathing review.'
    >>> browser.getControl(name='documentID').value = u'IPDA-XYZ-TN-592_3_7_2009JAN22-BOLLOCKS'
    >>> browser.getControl(name='text').value = u'Seriously, the guy has no clue.'
    >>> browser.getControl(name='form.button.save').click()
    >>> 'jz-secret-code-or-stupid-git' in portal.objectIds()
    True
    >>> theItem = portal['jz-secret-code-or-stupid-git']
    >>> theItem.documentID
    'IPDA-XYZ-TN-592_3_7_2009JAN22-BOLLOCKS'

Now the IPDA File, which is just like a regular file but with the document
ID::

    >>> fakeFile = cStringIO.StringIO("In-band signalling sucks-and that's all this is.")
    >>> browser.open(portalURL)
    >>> browser.getLink(id='ipda-file').url.endswith('createObject?type_name=IPDA+File')
    True
    >>> browser.getLink(id='ipda-file').click()
    >>> browser.getControl(name='title').value = u"Zender'ed"
    >>> browser.getControl(name='description').value = u"Ben Stiller's masterwork"
    >>> browser.getControl(name='documentID').value = u'IPDA-XYZ-TN-592_3_7_2009JAN22-BLOODY-HELL'
    >>> browser.getControl(name='file_file').add_file(fakeFile, 'application/pdf', 'zendered.pdf')
    >>> browser.getControl(name='form.button.save').click()
    >>> 'zendered.pdf' in portal.objectIds()
    True
    >>> theItem = portal['zendered.pdf']
    >>> theItem.documentID
    'IPDA-XYZ-TN-592_3_7_2009JAN22-BLOODY-HELL'


Steering Committee Display
~~~~~~~~~~~~~~~~~~~~~~~~~~

The Steering Committee Display is a simple object that shows some text,
provides a listing of IPDA steering committee members, and a search for
additional members.  First, let's make a steering committee:

    >>> portal.acl_users._doAddUser('maria', 'secret', [], [])
    <PloneUser 'maria'>
    >>> portal.acl_users._doAddUser('dan', 'secret', [], [])
    <PloneUser 'dan'>
    >>> portal.acl_users.source_groups.addGroup('SC', 'SC', 'Steering Committee')
    True
    >>> portal.acl_users.source_groups.addPrincipalToGroup('maria', 'SC')
    True
    >>> portal.acl_users.source_groups.addPrincipalToGroup('dan', 'SC')
    True

And we'll explicitly keep someone out:

    >>> portal.acl_users._doAddUser('zenderino', 'secret', [], [])
    <PloneUser 'zenderino'>

Although addable anywhere, a Steering Committee Display is nominally installed
in the site root only::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='steering-committee-display')
    >>> l.url.endswith('createObject?type_name=Steering+Committee+Display')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = 'SC'
    >>> browser.getControl(name='description').value = 'Steering Committee'
    >>> browser.getControl(name='form.button.save').click()
    >>> 'sc' in portal.objectIds()
    True
    >>> sc = portal['sc']
    >>> sc.title
    'SC'
    >>> sc.description
    'Steering Committee'

Now, are the group members there, and in alphabetical order?  Checking::

    >>> browser.contents
    '...dan...maria...'
    
And zenderino is *not* there::

    >>> 'zenderino' not in browser.contents
    True

In an email from Dan Crichton on 2011-1-25, apparently the Technical Experts
Group (TEG) is now special enough that they too warrant a section on the
display.  Fair enough.  Let's add the TEG::

    >>> portal.acl_users.source_groups.addGroup('TEG', 'TEG', 'Technical Experts Group')
    True

And we'll populate this group with some users, say "dan" and "zenderino"::

    >>> portal.acl_users.source_groups.addPrincipalToGroup('dan', 'TEG')
    True
    >>> portal.acl_users.source_groups.addPrincipalToGroup('zenderino', 'TEG')
    True

Now let's re-visit the page and see if things have changed::

    >>> browser.open(portalURL + '/sc')
    >>> browser.contents
    '...dan...maria...Technical Experts Group...dan...zenderino...'

Perfect.


Portlets
--------

As shown above, IPDA subclasses the standard Plone Event to make an IPDA
Event.  Sadly, Plone's Events portlet looks solely for Event objects (based on
``portal_type``) and not their subclasses (using ``object_provides``).  So, we
need our own Event portlet.  First, we'll add the portlet::

    >>> from ipdasite.projectmgmt.portlets import events
    >>> from zope.container.interfaces import INameChooser
    >>> col = getUtility(IPortletManager, name=u'plone.leftcolumn')
    >>> manager = getMultiAdapter((self.portal, col), IPortletAssignmentMapping)
    >>> assignment = events.Assignment()
    >>> chooser = INameChooser(manager)
    >>> manager[chooser.chooseName(None, assignment)] = assignment

Since we added events above, the portlet should appear::
    
    >>> browser.open(portalURL)
    >>> browser.contents
    '...<div...class="portletWrapper...Upcoming Events...Grand Poobah Council...</div>...'

That's it.

.. References:
.. _`International Planetary Data Alliance`: http://planetarydata.org/
