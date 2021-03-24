IPDA Website Installation
=========================

Installing the IPDA web site software requires the following packages be
available:

* Unix of some flavor
* Python_ 2.7 (plus development libraries and headers, ``python2.7-dev``)
* libjpeg_ (plus development libraries and headers, ``libjpeg62-dev``)
* PDF Poppler_ Utilities, ``poppler-utils``
* wvWare_ (also known as ``wv``)
* Lynx_
* Build tools: C/C++ compiler, make, etc. (the ``build-essential`` package)
* Varnish_ 3
* Nginx_ 1.0

You'll also need a non-privileged user account to run the software. For the
purposes of this document, we'll call this user $USER.

You'll also need root privileges, such as provided by the ``sudo`` command.


Set Up
------

Make a Unix user account and directory to contain the IPDA site software suite,
e.g.::

    useradd --comment 'Intl Planetary Data Alliance' \
        --home /usr/local/ipda \
        --create-home --system


Extract the tarball in that directory if it doesn't already exist::

    cd /usr/local/ipda
    sudo tar xjf ~/ipdasite-VERSION.tar.bz2
    sudo chown -R ipda:ipda ipdasite-VERSION


Deploy It
---------

Run the ``deploy.py`` script.  Use ``--help`` to see all the options.  Typically
you'll include the directory of the previous version of the site as the final
positional argument.  Run the ``deploy.py`` script with Python 2.7.

Example (first time setup, testing hostname)::

    sudo -u ipda /usr/local/python-2.7.6/bin/python2.7 ./deploy.py \
        --buildout-cache /usr/local/ipda/buildout \
        --with-wvHtml /usr/local/wv-1.2.4/bin/wvHtml \
        --libdir /usr/local/libxml2-2.9.1/lib \
        --libdir /usr/local/libxslt-1.1.28/lib \
        --public-hostname pds-starlight.jpl.nasa.gov \
        /usr/local/backup/ipdasite

Example (upgrade from version 2.0.3, planetarydata.org hostname (default))::

    sudo -u ipda /usr/local/python-2.7.6/bin/python2.7 ./deploy.py \
        --buildout-cache /usr/local/ipda/buildout \
        --with-wvHtml /usr/local/wv-1.2.4/bin/wvHtml \
        --libdir /usr/local/libxml2-2.9.1/lib \
        --libdir /usr/local/libxslt-1.1.28/lib \
        /usr/local/ipdasite/ipdasite-2.0.3

Note that running ``deploy.py`` the first time can take a long time as it
downloads all of the component parts of Plone, Zope, Tomcat, Registry Service,
and all dependencies.  Now would be a good time for a sandwich.


Decode the SSL Key
------------------

After deploying, run:

    openssl rsa -in etc/certs/planetarydata.org.key -out etc/certs/planetarydata.org.key.unencrypted

Give the passphrase to the key when prompted.


Hooking Into Operating System Services
--------------------------------------

You'll need to enable the operating system services (cron jobs, log file
rotation, and init scripts).

The cron jobs perform daily backups of the site database, weekly database
snapshots, and monthly database packing.  To set this up, enter these
commands::

    sudo install -o root -g root -m 755 bin/backup /etc/cron.daily/ipda-backup
    sudo install -o root -g root -m 755 bin/snapshotbackup /etc/cron.weekly/ipda-snapshot
    sudo install -o root -g root -m 755 bin/zeopack /etc/cron.monthly/ipda-pack

Next, set up logfile rotation by running::

    sudo install -o root -g root -m 644 parts/templates/logrotate.cfg /etc/logrotate.d/ipda

Finally, install an init.d rc startup script so that the IPDA website can be
started at boot time and stopped at shutdown time.  To do so, enter::

    sudo install -o root -g root -m 755 parts/templates/ipda /etc/init.d

On some operating systems, you'll need to set up symbolic links using a
command like ``chkconfig --add ipda`` or ``update-rc.d``.  Consult your OS
documentation for details.


Starting and Viewing the Site
-----------------------------

Finally, you can start the website::

    sudo /etc/init.d/ipda start

(Or substitute an equivalent command for your operating system.) You can check
the process supervisor by running ``bin/supervisorctl``; you should see five
processes in the RUNNING state.

Visit the site at http://planetarydata.org/.


Setting the "Current" Symlink
-----------------------------

For convenience, remove any existing /usr/local/ipda/current symlink and link it
to the newly installed version::

    cd ..
    sudo rm current
    sudo ln -s ipdasite-VERSION current



.. References:
.. _buildout: http://www.buildout.org/
.. _debian: http://www.debian.org/
.. _libjpeg: http://python.org/
.. _nginx: http://wiki.nginx.org/Main
.. _plone: http://plone.org/
.. _poppler: http://poppler.freedesktop.org/
.. _python: http://python.org/
.. _supervisor: http://supervisord.org/
.. _varnish: https://www.varnish-cache.org/
.. _wvware: http://wvware.sourceforge.net/
.. _zope: http://zope.org/
