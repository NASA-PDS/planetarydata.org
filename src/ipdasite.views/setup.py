# encoding: utf-8
# Copyright 2012–2014 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from setuptools import setup, find_packages
import os.path

# Package data
# ------------

_name        = 'ipdasite.views'
_version     = '1.0.3'
_description = 'International Planetary Data Alliance: Website: Views'
_url         = 'http://pypy.python.org/pypi/ipdasite.views'
_downloadURL = 'http://oodt.jpl.nasa.gov/dist/ipdasite'
_author      = 'Sean Kelly'
_authorEmail = 'sean.kelly@jpl.nasa.gov'
_license     = 'Proprietary'
_namespaces  = ['ipdasite']
_zipSafe     = False
_keywords    = 'web zope plone planetary data views ipda'
_entryPoints = {'z3c.autoinclude.plugin': ['target=plone']}
_extras      = {'test': ['plone.app.testing', 'Pillow']}
_externalRequirements = [
    'setuptools',
    'Products.CMFPlone',
    'plone.app.dexterity[relations]',
    'z3c.autoinclude',
    'five.grok',
]
_classifiers = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Web Environment',
    'Framework :: Plone',
    'Intended Audience :: Science/Research',
    'License :: Other/Proprietary License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

# Setup Metadata
# --------------

def _read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

_header = '*' * len(_name) + '\n' + _name + '\n' + '*' * len(_name)
_longDescription = _header + '\n\n' + _read('README.txt') + '\n\n' + _read('docs', 'INSTALL.txt') + '\n\n' \
    + _read('docs', 'HISTORY.txt') + '\n\n' + _read('docs', 'LICENSE.txt')
open('doc.txt', 'w').write(_longDescription)

setup(
    author=_author,
    author_email=_authorEmail,
    classifiers=_classifiers,
    description=_description,
    download_url=_downloadURL,
    entry_points=_entryPoints,
    extras_require=_extras,
    include_package_data=True,
    install_requires=_externalRequirements,
    keywords=_keywords,
    license=_license,
    long_description=_longDescription,
    name=_name,
    namespace_packages=_namespaces,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url=_url,
    version=_version,
    zip_safe=_zipSafe,
)
