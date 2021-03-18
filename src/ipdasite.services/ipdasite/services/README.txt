The IPDA_ Service Registry provides an ebXML_ styled object registry
specifically for Services and their related objects.  This enables the IPDA to
register, look up, and access various services provided by IPDA and its member
institutions, all through a convenient web user interface hosted at the IPDA
web site.

This package, ``ipdasite.services``, introduces the IPDA Service Registry
implementation (and also provides functional tests).


Summary of Classes
==================

The classes this package provides include the following:

Service Registry
    A top-level container for service definitions and their related objects.
Curator
    An agent (person, institution, etc.) responsible for services.
Service
    Something that provides a use to external software.
Service Binding
    An endpoint of a Service.
Specification Link
    Tells how to use the a Service Binding.


Functional Tests
================

The document you're reading can also be "executed" (using the testing
framework) in order to provide functional tests of the ``ipdasite.services``
classes.  In order to execute these tests, we'll first need a test browser::

    >>> app = layer['app']
    >>> from plone.testing.z2 import Browser
    >>> from plone.app.testing import SITE_OWNER_NAME, SITE_OWNER_PASSWORD
    >>> browser = Browser(app)
    >>> browser.handleErrors = False
    >>> browser.addHeader('Authorization', 'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
    >>> portal = layer['portal']    
    >>> portalURL = portal.absolute_url()

For some demonstrations below, we'll also need a browser that's not logged in,
to prove that items that require permissions work as expected::

    >>> unprivilegedBrowser = Browser(app)
    >>> unprivilegedBrowser.handleErrors = False

Finally, we're ready to dive into the classes provided by
``ipdasite.services``.


The Service Registry
====================

All the action starts with objects of class Service Registry.  A Service
Registry object is an instance of a single registry (in the ebXML sense), but
specialized for the IPDA to be compatible with the PDS_ and its notion of a
registry.  We can create a Service Registry anywhere within the IPDA site, so
why not at the root?  Here goes::

    >>> browser.open(portalURL)
    >>> l = browser.getLink(id='service-registry')
    >>> l.url.endswith('createObject?type_name=Service+Registry')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'My Service Registry'
    >>> browser.getControl(name='description').value = u'A sample registry for testing purposes.'
    >>> browser.getControl(name='home').value = u'http://planetarydata.org/registry-service'
    >>> browser.getControl(name='sync:boolean').value = False
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink(id='workflow-transition-publish').click()
    >>> 'my-service-registry' in portal.keys()
    True
    >>> registry = portal['my-service-registry']
    >>> registry.title
    'My Service Registry'
    >>> registry.description
    'A sample registry for testing purposes.'
    >>> registry.home
    'http://planetarydata.org/registry-service'
    >>> registry.sync
    False

When creating a Service Registry, the "home" field should be a valid URL.
What happens if it's not?  Let's find out::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='service-registry').click()
    >>> browser.getControl(name='title').value = u'Bad URL'
    >>> browser.getControl(name='home').value = u'Baaaaaad URL!'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.contents
    '...is not a valid url...'

Good.  Let's open up our sample Service Registry::

    >>> browser.open(portalURL + '/my-service-registry')

Can we edit it once it's created?  Clicking the Edit tab::

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='description').value = u'Just for functional tests.'
    >>> browser.getControl(name='home').value = u'http://planetarydata.org:8080/registry-service'
    >>> browser.getControl(name='form.button.save').click()

The fields were updated::

    >>> registry.description
    'Just for functional tests.'
    >>> registry.home
    'http://planetarydata.org:8080/registry-service'

Looking good.  But this Service Registry has no services in it.  See for yourself:

    >>> browser.open(portalURL + '/my-service-registry')
    >>> browser.contents
    '...There are currently no services registered in this registry...'

Further, there are no curators for services::

    >>> browser.contents
    '...There are currently no curators listed in this registry...'

We'll soon remedy that, below.  But before we do, also note that there's an
extra large pretty buttons to press that lets you add new services and
curators::

    >>> browser.contents
    '...Creates a new service or tool in this registry...Creates a new curator...'

That appears because we're logged in as an administrator.  But an anonymous
viewer gets no such button::

    >>> unprivilegedBrowser.open(portalURL + '/my-service-registry')
    >>> 'Creates a new curator' in unprivilegedBrowser.contents
    False
    >>> 'Creates a new service in this registry' in unprivilegedBrowser.contents
    False


Curators Curate Services
========================

Some of the data we capture in the Service registry are the people who are
responsible for creating, deploying, and maintaining these services.  We call
them Curators, and they can be created solely within the Service Registry::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='curator')
    Traceback (most recent call last):
    ...
    LinkNotFoundError

See?  Now, if we try again in the actual Service Registry::

    >>> browser.open(portalURL + '/my-service-registry')
    >>> l = browser.getLink(id='curator')
    >>> l.url.endswith('createObject?type_name=Curator')
    True
    >>> l.click()
    >>> browser.getControl(name='title').value = u'National Oceanic and Atmospheric Administration'
    >>> browser.getControl(name='description').value = u'NOAA focuses on oceans and atmosphere, weather and stuff.'
    >>> browser.getControl(name='contactName').value = u'Jane Lubchenco'
    >>> browser.getControl(name='emailAddress').value = u'jane.lubchenco@noaa.gov'
    >>> browser.getControl(name='telephone').value = u'+1 828 271 4800'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink(id='workflow-transition-publish').click()
    >>> 'national-oceanic-and-atmospheric-administration' in registry.keys()
    True
    >>> curator = registry['national-oceanic-and-atmospheric-administration']
    >>> curator.title
    'National Oceanic and Atmospheric Administration'
    >>> curator.description
    'NOAA focuses on oceans and atmosphere, weather and stuff.'
    >>> curator.contactName
    'Jane Lubchenco'
    >>> curator.emailAddress
    'jane.lubchenco@noaa.gov'
    >>> curator.telephone
    '+1 828 271 4800'

OK, whoop-de-doo.  Let's create a Service.


A Service
=========

Services are, of course, the whole point of the Service Registry.  Service
objects can't be added just anywhere on the web site, though::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='service')
    Traceback (most recent call last):
    ...
    LinkNotFoundError

They belong in Service Registry objects::

    >>> browser.open(portalURL + '/my-service-registry')
    >>> l = browser.getLink(id='service')
    >>> l.url.endswith('createObject?type_name=Service')
    True
    >>> l.click()
    >>> browser.getControl(name='guid').value = 'urn:uuid:2968497b-8d85-42f5-9309-9f20a533ea9f'
    >>> browser.getControl(name='lid').value = u'urn:wx:temp-1.0.0'
    >>> browser.getControl(name='title').value = u'Weather Temperature Service'
    >>> browser.getControl(name='description').value = u'A service that provides current air temperature readings.'
    >>> browser.getControl(name='toolURL').value = u'http://wx.com/tools/download'
    >>> browser.getControl(name='versionID').value = u'1.0.0'
    >>> browser.getControl(name='releaseDate_year').displayValue = ['2005']
    >>> browser.getControl(name='releaseDate_month').value = ['07']
    >>> browser.getControl(name='releaseDate_day').value = ['15']
    >>> browser.getControl(name='abstract').value = u'<p>Well, you <em>call</em> it and it tells you how <em>warm</em> it is.</p>'
    >>> browser.getControl(name='requirements').value = u"You'll need an internet connection."
    >>> browser.getControl('National Oceanic and Atmospheric Administration').selected = True
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink(id='workflow-transition-publish').click()
    >>> 'weather-temperature-service' in registry.keys()
    True
    >>> tempService = registry['weather-temperature-service']
    >>> tempService.guid
    'urn:uuid:2968497b-8d85-42f5-9309-9f20a533ea9f'
    >>> tempService.lid
    'urn:wx:temp-1.0.0'
    >>> tempService.title
    'Weather Temperature Service'
    >>> tempService.description
    'A service that provides current air temperature readings.'
    >>> tempService.toolURL
    'http://wx.com/tools/download'
    >>> tempService.versionID
    '1.0.0'
    >>> tempService.releaseDate.year(), tempService.releaseDate.month(), tempService.releaseDate.day()
    (2005, 7, 15)
    >>> tempService.abstract
    '<p>Well, you <em>call</em> it and it tells you how <em>warm</em> it is.</p>'
    >>> tempService.requirements
    "You'll need an internet connection."
    >>> tempService.curator.UID() == curator.UID()
    True

Services (and indeed all identifiable objects within a registry) have,
according to ebXML, a "home" attribute that tells what registry they come
from.  Thanks to Zope's acquisition feature, our Service object above gets
that for free::

    >>> tempService.home == registry.home
    True
    >>> tempService.home
    'http://planetarydata.org:8080/registry-service'

The globally unique ID for a Service is optional.  If it's left blank, the
service registry should assign one automatically.  Also, the version ID will
default to a known value::

    >>> browser.open(portalURL + '/my-service-registry')
    >>> browser.getLink(id='service').click()
    >>> browser.getControl(name='lid').value = u'urn:wx:wind-0.0.0'
    >>> browser.getControl(name='title').value = u'Weather Wind Service'
    >>> browser.getControl(name='description').value = u'A service that provides current wind velocity readings.'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink(id='workflow-transition-publish').click()
    >>> windService = registry['weather-wind-service']
    >>> windService.guid
    'urn:uuid:...-...-...-...-...'
    >>> windService.versionID
    '0.0.0'

One thing I've noticed when trying to integrate this package with the PDS
Service Registry (http://pdscm.jpl.nasa.gov/2010/registry/registry-service/)
is that the PDS Registry Service enforces unique logical IDs, while Emily Law
has been fond of using "TBD" as the same logical ID for services.  Will our
package enforce unique logical IDs?

To find out, let's create another service that re-uses the logical ID as the
service just above::

    >>> browser.open(portalURL + '/my-service-registry')
    >>> browser.getLink(id='service').click()
    >>> browser.getControl(name='lid').value = u'urn:wx:wind-0.0.0'
    >>> browser.getControl(name='title').value = u'Weather Radar Service'
    >>> browser.getControl(name='description').value = u'A service that provides radar data.'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.contents
    '...The logical ID is already in use...'

Good.


Service Bindings
================

The "Service" objects we created above don't actually say much about the
services except that they exist.  However, the ebXML model anticipated this
and so added another item to the model called a Service Binding.  They tell
where to access a service.  Now, PDS-EN management felt IPDA wanted a Service
Registry based on ebXML, and that's what we did here.  But that's not what
IPDA really needed.  IPDA needed a tool registry.  We sort of forced this
service registry model into registering tools, where service bindings and
specification links don't make sense.

However, Service Bindings still exist in the system, and they belong to
Service objects.  As such, you can't add them just anywhere::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='service-binding')
    Traceback (most recent call last):
    ...
    LinkNotFoundError

Only to Service objects:

    >>> browser.open(portalURL + '/my-service-registry/weather-temperature-service')
    >>> l = browser.getLink(id='service-binding')
    >>> l.url.endswith('createObject?type_name=Service+Binding')
    True
    >>> l.click()
    >>> browser.getControl(name='guid').value = 'urn:uuid:f4f9f150-193e-42f6-8d24-3d42a5154fbe'
    >>> browser.getControl(name='lid').value = u'http://wx.org/xmlrpc/temp'
    >>> browser.getControl(name='accessURI').value = u'http://wx.org/xmlrpc/temp'
    >>> browser.getControl(name='title').value = u'Temperature via XML-RPC'
    >>> browser.getControl(name='description').value = u'XML-RPC-based web service that gives temperatures by coordinates.'
    >>> browser.getControl(name='versionID').value = u'1.0.0'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink(id='workflow-transition-publish').click()

The most important part of the Service Binding is the access URI, which gives
an endpoint for accessing the service.  According to ebXML, Service Bindings
are also Registry Objects, so they have "logical IDs" or "lids".  However, the
PDS doesn't really use them.  Conventionally, we just set the "lid" equal to
the access URI.  Let's check out our newly created Service Binding::

    >>> 'temperature-via-xml-rpc' in tempService.keys()
    True
    >>> xmlRPCBinding = tempService['temperature-via-xml-rpc']
    >>> xmlRPCBinding.guid
    'urn:uuid:f4f9f150-193e-42f6-8d24-3d42a5154fbe'
    >>> xmlRPCBinding.lid
    'http://wx.org/xmlrpc/temp'
    >>> xmlRPCBinding.accessURI
    'http://wx.org/xmlrpc/temp'
    >>> xmlRPCBinding.title
    'Temperature via XML-RPC'
    >>> xmlRPCBinding.description
    'XML-RPC-based web service that gives temperatures by coordinates.'
    >>> xmlRPCBinding.versionID
    '1.0.0'

Looks good.  As with the Service, the GUID and versionID will default to certain
values if not given::

    >>> browser.open(portalURL + '/my-service-registry/weather-temperature-service')
    >>> browser.getLink(id='service-binding').click()
    >>> browser.getControl(name='lid').value = u'http://wx.org/rest/temp'
    >>> browser.getControl(name='accessURI').value = u'http://wx.org/rest/temp'
    >>> browser.getControl(name='title').value = u'Temperature via REST'
    >>> browser.getControl(name='description').value = u'REST-based web service that gives temperatures by coordinates.'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink(id='workflow-transition-publish').click()
    >>> restBinding = tempService['temperature-via-rest']
    >>> restBinding.guid
    'urn:uuid:...-...-...-...-...'
    >>> restBinding.versionID
    '0.0.0'

Service Bindings are supposed to support a "target binding" attribute as well.
However, since we really want to get this implementation out the door, we'll
omit that for now and revisit it in a later implementation.

Issue IPDA-50 noticed that the New Service Binding button wasn't appearing.  Is
that the case?  Let's find out::

    >>> browser.open(portalURL + '/my-service-registry/weather-temperature-service')
    >>> 'New Service Binding' in browser.contents
    True

No problem.


Specification Links
===================

The Service Binding identifies the endpoint (the access URI) of a Service.
However, even with that, you still don't know how to invoke the service.
Sure, you could guess.  Go ahead, guess.  I dare you.

Failed miserably?  Typical.  Now keep reading.

Specification Link objects tell you how to use the Service Binding's access
URI, by giving you pointers to usage documents like WSDL files, CORBA (which
sucks) IDL files, and so forth.  Since they link to usage documents, let's
populate our site with a sample document::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='document').click()
    >>> browser.getControl(name='title').value = u'Using the XML-RPC Temperature Service'
    >>> browser.getControl(name='description').value = u'An introduction to using the XML-RPC flavor of the temperature service.'
    >>> browser.getControl(name='text').value = u'<p>First, and then, finally.</p>'
    >>> browser.getControl(name='form.button.save').click()
    >>> specObj = portal['using-the-xml-rpc-temperature-service']

Specification Links belong only in Service Binding objects and thus can be
added only to them::

    >>> browser.open(portalURL)
    >>> browser.getLink(id='specification-link')
    Traceback (most recent call last):
    ...
    LinkNotFoundError
    >>> browser.open(portalURL + '/my-service-registry/weather-temperature-service/temperature-via-xml-rpc')
    >>> l = browser.getLink(id='specification-link')
    >>> l.url.endswith('createObject?type_name=Specification+Link')
    True
    >>> l.click()
    >>> browser.getControl(name='guid').value = 'urn:uuid:8baffedc-e1d0-4299-abb5-892850065f95'
    >>> browser.getControl(name='lid').value = specObj.absolute_url()
    >>> browser.getControl(name='title').value = u'Calling the XML-RPC Temperature Service'
    >>> browser.getControl(name='description').value = u'A kind of README for the XML-RPC service for temperature readings.'
    >>> browser.getControl(name='versionID').value = u'1.0.0'
    >>> browser.getControl(name='specificationObject').value = specObj.UID()
    >>> browser.getControl(name='usageDescription').value = u'You can also pass a "units" parameter.'
    >>> browser.getControl(name='usageParameters:lines').value = u'C\nF\nK'
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink(id='workflow-transition-publish').click()
    
The most important part of the Specification Link is the specification object,
which identifies some other object on the site that serves as the official
specification for accessing the service.  The usage description and usage
parameters are also helpful, but they're optional.  According to ebXML,
Specification Links are, like Service Bindings, also Registry Objects.  As
such, they have "logical IDs" or "lids".  The PDS doesn't really use them,
though.  Checking out our newly created Specification Link, we find::

    >>> 'calling-the-xml-rpc-temperature-service' in xmlRPCBinding.keys()
    True
    >>> xmlRPCSpecLink = xmlRPCBinding['calling-the-xml-rpc-temperature-service']
    >>> xmlRPCSpecLink.guid
    'urn:uuid:8baffedc-e1d0-4299-abb5-892850065f95'
    >>> xmlRPCSpecLink.lid == specObj.absolute_url()
    True
    >>> xmlRPCSpecLink.title
    'Calling the XML-RPC Temperature Service'
    >>> xmlRPCSpecLink.description
    'A kind of README for the XML-RPC service for temperature readings.'
    >>> xmlRPCSpecLink.versionID
    '1.0.0'
    >>> xmlRPCSpecLink.specificationObject.UID() == specObj.UID()
    True
    >>> xmlRPCSpecLink.usageDescription
    'You can also pass a "units" parameter.'
    >>> xmlRPCSpecLink.usageParameters
    ('C', 'F', 'K')

Looks good.  Note that the GUID and versionID will default to certain values if not given::

    >>> browser.open(portalURL + '/my-service-registry/weather-temperature-service/temperature-via-xml-rpc')
    >>> browser.getLink(id='specification-link').click()
    >>> browser.getControl(name='lid').value = specObj.absolute_url() + '/2'
    >>> browser.getControl(name='title').value = u'Redundant Specification Link'
    >>> browser.getControl(name='specificationObject').value = specObj.UID()
    >>> browser.getControl(name='form.button.save').click()
    >>> browser.getLink(id='workflow-transition-publish').click()
    >>> redundantLink = xmlRPCBinding['redundant-specification-link']
    >>> redundantLink.guid
    'urn:uuid:...-...-...-...-...'
    >>> redundantLink.versionID
    '0.0.0'


Service Registry View
=====================

We saw above what appeared when a Service Registry was empty.  It wasn't very
interesting.  However, now that we have some curators and services registered
and they have service bindings, the display ought to be quite a bit more
enthralling (however enthralling a service registry can be).  First off, note
how items are ordered by title by default::

    >>> browser.open(portalURL + '/my-service-registry')
    >>> browser.contents
    '...Services...Temperature Service...Wind Service...Curators...National Oceanic...'

Version numbers of services also appear::

    >>> browser.contents
    '...Temperature Service...1.0.0...Wind Service...0.0.0...'

Bindings used to appear, however since this is supposed to be a tool registry,
not a service registry, they don't anymore::

    >>> 'Temperature via REST' in browser.contents
    False
    >>> 'Temperature via XML-RPC' in browser.contents
    False
    >>> 'There are no bindings defined for this service' in browser.contents
    False


Service View
============

Viewing a Service shows its attributes, but not the bindings that are present
for it::

    >>> browser.open(portalURL + '/my-service-registry/weather-temperature-service')
    >>> browser.contents
    '...2005/07/15...urn:wx:temp-1.0.0...urn:uuid:2968497b...'
    >>> 'Bindings' in browser.contents
    False

All the additional slots (abstract, OS, requirements, source, contact
information, tool URL) are all there::

    >>> browser.open(portalURL + '/my-service-registry/weather-temperature-service')
    >>> '<p>Well, you <em>call</em> it and it tells you how <em>warm</em> it is.</p>' in browser.contents
    True
    >>> "You'll need an internet connection." in browser.contents
    True
    >>> 'http://wx.com/tools/download' in browser.contents
    True

The extra large pretty button to press that lets you add a new binding is gone::

    >>> 'Creates a new binding of this service' in browser.contents
    False


Service Binding View
====================

Viewing a Service Binding simply displays its various attributes::

    >>> browser.open(portalURL + '/my-service-registry/weather-temperature-service/temperature-via-xml-rpc')
    >>> browser.contents
    '...Access URI...http://wx.org/xmlrpc/temp...Version...1.0.0...Logical...http://wx.org/xmlrpc/temp...'
    
Followed by any Specification Links::

    >>> browser.contents
    '...Specification Links...Calling the XML-RPC Temperature Service...Redundant Specification Link...'

And a binding with no Specification Links says so::

    >>> browser.open(portalURL + '/my-service-registry/weather-temperature-service/temperature-via-rest')
    >>> browser.contents
    '...There are currently no specification links defined for this service...'

Note also there's an extra large pretty button to press that lets you add a
new binding::

    >>> browser.contents
    '...Creates a new specification link for this binding...'

We allow the specification link button because you have to be an advanced user
to actually add a Service Binding, and adding a Specification Link is a nice
reward.

Also, the button appears because we're logged in as someone with permissions
to add specification links.  Anonymous users see no such button::

    >>> unprivilegedBrowser.open(portalURL + '/my-service-registry/weather-temperature-service/temperature-via-rest')
    >>> 'Creates a new specification link for this binding' in unprivilegedBrowser.contents
    False


Specification Link View
=======================

Viewing a Specification Link merely shows its attributes::

    >>> browser.open(portalURL + '/my-service-registry/weather-temperature-service/temperature-via-xml-rpc/calling-the-xml-rpc-temperature-service')
    >>> browser.contents
    '...Specification...Using the XML-RPC Temperature Service...Usage Description...You can also pass a "units" parameter...'
    >>> browser.contents
    '...Usage Parameters...C...F...K...'

That's pretty much it.



.. References:
.. _IPDA: http://planetarydata.org/
.. _ebXML: http://www.oasis-open.org/committees/tc_home.php?wg_abbrev=regrep
.. _portlets: http://en.wikipedia.org/wiki/Portlet
.. _PDS: http://pds.nasa.gov/
