#!/usr/bin/env python
# encoding: utf-8
# Copyright 2014 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.
#
# deploy.py - Deploy the IPDA site into operations

import argparse, sys, logging, os, os.path, re, subprocess, pwd, urllib2, contextlib, tempfile, tarfile, string, random
import shutil

reload(sys)
sys.setdefaultencoding('utf-8')

_bufsiz = 512
_buildoutCache = u'/apps/ipdasite/buildout'
_setupToolsVersion = u'23.0.0'
_virtualEnvVersion = u'15.0.2'
_buildoutVersion = u'2.5.2'
_virtualEnvURL = u'https://pypi.python.org/packages/source/v/virtualenv/virtualenv-{}.tar.gz'.format(_virtualEnvVersion)

_cHeader = '''#ifdef __cplusplus
extern "C"
#endif
'''

class DeploymentError(Exception):
    pass
    
def _setupLogging():
    logging.basicConfig(level=logging.DEBUG, format=u'%(asctime)s %(levelname)-8s %(message)s',
        filename=u'deploy.log', filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(u'%(message)s'))
    logging.getLogger('').addHandler(console)
    logging.debug(u'Logging configured')

def _getArgParser():
    p = argparse.ArgumentParser(
        description=u'Deploys the IPDA web site and services in this directory. If a previous installation'
            u' exists, give its path on the command-line, and its content will be migrated over.  Otherwise,'
            u' an empty, content-free website will be deployed.',
        epilog=u'For more information or help, contact sean.kelly@jpl.nasa.gov.'
    )
    p.add_argument(u'existing', nargs='?', help=u'Path to existing IPDA website installation for content')
    p.add_argument(u'--buildout-cache', metavar=u'PATH', default=_buildoutCache,
        help=u'Use cached downloads/eggs/extends in %(metavar)s instead of %(default)s')
    p.add_argument(u'--libdir', metavar=u'PATH', action='append',
        help=u'Add %(metavar)s to the list of dirs to check for libraries; repeat this option as needed')

    g = p.add_argument_group(u'Internet', u'Hostnames and ports.')
    g.add_argument(u'--public-hostname', metavar=u'HOSTNAME',
        help=u'Override the default hostname "%(default)s" with %(metavar)s', default=u'planetarydata.org')
    g.add_argument(u'--http-port', metavar=u'PORTNUM', type=int, default=80,
        help=u'Override the default HTTP port %(default)d with %(metavar)s')
    g.add_argument(u'--https-port', metavar=u'PORTNUM', type=int, default=443,
        help=u'Override the default HTTPS port %(default)d with %(metavar)s')

    g = p.add_argument_group(u'Usernames & Passwords', u'Random passwords will be generated unless specified below.')    
    g.add_argument(u'--supervisor-user', metavar=u'USERNAME', default=u'supervisor-admin',
        help=u'Override the Supervisor username "%(default)s" with %(metavar)s')
    g.add_argument(u'--supervisor-password', metavar=u'PASSWORD', help='Use %(metavar)s insetad of a random password')
    g.add_argument(u'--tomcat-user', metavar=u'USERNAME', default=u'tomcat-admin',
        help=u'Override the Tomcat username "%(default)s" with %(metavar)s')
    g.add_argument(u'--tomcat-password', metavar=u'PASSWORD', help=u'Use %(metavar)s instead of a random password')
    g.add_argument(u'--zope-user', metavar=u'USERNAME', default=u'zope-admin',
        help=u'Override the Zope app server username "%(default)s" with %(metavar)s')
    g.add_argument(u'--zope-password', metavar=u'PASSWORD', help=u'Use %(metavar)s instead of a random password')

    g = p.add_argument_group(u'Executables', u'These will be searched on the executable PATH unless overridden.')
    g.add_argument(u'--with-java',       metavar=u'PATH', help=u'Use the Java language at %(metavar)s')
    g.add_argument(u'--with-lynx',       metavar=u'PATH', help=u'Use the lynx plain-text browser at %(metavar)s')
    g.add_argument(u'--with-nginx',      metavar=u'PATH', help=u'Use the nginx web server at %(metavar)s')
    g.add_argument(u'--with-pdftohtml',  metavar=u'PATH', help=u'Use the pdftohtml converter at %(metavar)s')
    g.add_argument(u'--with-varnishd',   metavar=u'PATH', help=u'Use the varnishd cache at %(metavar)s')
    g.add_argument(u'--with-wvHtml',     metavar=u'PATH', help=u'Use the wvHtml Word converter at %(metavar)s')
    g.add_argument(u'--with-python',     metavar=u'PATH', help=u'Use the Python language at %(metavar)s',
        default=sys.executable)
    return p

def _findExecutable(name, location=None):
    logging.debug(u'Looking for executable "%s"%s', name,
        u' (Possibly at {})'.format(location) if location is not None else u'')
    if location:
        if not os.path.isfile(location):
            raise DeploymentError(u'The "{}" at "{}" is not a file'.format(name, location))
        if not os.access(location, os.X_OK):
            raise DeploymentError(u'The "{}" at "{}" is not executable'.format(name, location))
        return location
    for d in os.environ['PATH'].split(u':'):
        candidate = os.path.join(d, name)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    raise DeploymentError(u'Executable "{}" not found in PATH'.format(name))

def _checkVarnish(path):
    logging.info('Checking varnishd version')
    output = subprocess.check_output([path, u'-V'], stderr=subprocess.STDOUT)
    if re.match(ur'varnishd \(varnish-3', output) is None:
        raise DeploymentError(u'Varnish at "{}" needs to be version 3+'.format(path))

def _findExecutables(namespace):
    logging.info('Finding dependent executables')    
    java = _findExecutable(u'java', namespace.with_java)
    logging.info(u'Using java at %s', java)
    nginx = _findExecutable(u'nginx', namespace.with_nginx)
    logging.info(u'Using nginx at %s', nginx)
    lynx = _findExecutable(u'lynx', namespace.with_lynx)
    logging.info(u'Using lynx at %s', lynx)
    pdftohtml = _findExecutable(u'pdftohtml', namespace.with_pdftohtml)
    logging.info(u'Using pdftohtml at %s', pdftohtml)
    varnishd = _findExecutable(u'varnishd', namespace.with_varnishd)
    logging.info(u'Using varnishd at %s', varnishd)
    wvHtml = _findExecutable(u'wvHtml', namespace.with_wvHtml)
    logging.info(u'Using wvHtml at %s', wvHtml)
    python = _findExecutable(u'python2.7', namespace.with_python)
    logging.info(u'Using python2.7 at %s', python)
    return dict(java=java, nginx=nginx, lynx=lynx, pdftohtml=pdftohtml, python=python, varnishd=varnishd, wvHtml=wvHtml)

def _checkLibrary(lib, func, libdirs):
    logging.debug('Checking for %s in %s (extra libdirs: %r)', func, lib, libdirs)
    fd, fn = tempfile.mkstemp(suffix='.c')
    out = os.fdopen(fd, 'w')
    out.write(_cHeader)
    out.write('char %s();\nint main() {\nreturn %s();}\n' % (func, func))
    out.close()
    args = ['cc', fn, '-l{}'.format(lib)]
    args.extend(['-L{}'.format(i) for i in libdirs])
    _execAndLog(args)
    os.remove('a.out')

def _checkLibraries(namespace):
    logging.info('Finding dependent libraries and headers')
    extraLibdirs = namespace.libdir
    if extraLibdirs is None:
        extraLibdirs = []
    for lib, func in (
        ('xml2', 'xmlNewEntity'),
        ('xslt', 'xsltInit'),
    ):
        logging.info('Checking for %s', lib)
        _checkLibrary(lib, func, extraLibdirs)
    # If we get here, then _checkLibrary didn't raise any exception and we found our symbols.
    # Note: we should also check versions.
    return extraLibdirs

def _getUserID():
    logging.info(u'Getting user ID')
    username = pwd.getpwuid(os.getuid())[0]
    logname = os.environ['LOGNAME']
    if logname != username:
        logging.warning("LOGNAME \"%s\" does not match current user ID's account name \"%s\", preferring latter",
            logname, username)
    return username

def _installVirtualEnv(python):
    logging.info(u'Installing virtualenv %s', _virtualEnvVersion)
    sentinel = os.path.join(u'virtualenv-{}'.format(_virtualEnvVersion),u'virtualenv_support',u'__init__.py')
    if not os.path.isfile(sentinel):
        logging.debug(u'Downloading from %s', _virtualEnvURL)
        with _download(_virtualEnvURL) as f:
            tf = tarfile.open(fileobj=f, mode='r:gz')
            tf.extractall()
    else:
        logging.debug(u'Found virtualenv already')
    sentinel = os.path.join(u'python2.7', 'bin', 'activate.csh')
    if not os.path.isfile(sentinel):
        logging.debug(u'Installing virtualenv for python2.7')
        ve = os.path.join(u'virtualenv-{}'.format(_virtualEnvVersion), u'virtualenv.py')
        subprocess.check_call([python, ve, u'python2.7'])
    else:
        logging.debug(u'Found virtualenv python already')
    # Check for upgraded setuptools?

def _checkCWD():
    logging.info(u"Checking what directory we're in")
    for name, test in (
        ('bootstrap.py', os.path.isfile),
        ('etc', os.path.isdir),
        ('ops.cfg', os.path.isfile),
        ('static', os.path.isdir),
        ('templates', os.path.isdir)
    ):
        if not test(name):
            raise DeploymentError(u"File/dir \"{}\" missing; are you running from the right directory?".format(name))

def _download(url):
    tf = tempfile.TemporaryFile()
    with contextlib.closing(urllib2.urlopen(url)) as con:
        while True:
            buf = con.read(_bufsiz)
            if len(buf) == 0:
                break
            tf.write(buf)
    tf.flush()
    tf.seek(0)
    return tf

def _installSiteConfig(
    executables, extraPaths, libdirs, superUser, superPassword, tomcatUser, tomcatPassword,
    zopeUser, zopePassword, hostname, http, https, userID, buildoutCache
):
    logging.info(u'Creating site.cfg')
    javaHome = os.path.dirname(os.path.dirname(executables['java']))
    with open(u'site.cfg', 'w') as f:
        f.write(u'[buildout]\n')
        f.write(u'extends = ops.cfg\n')
        for directive, directory in (
            (u'download-cache', u'downloads'),
            (u'eggs-directory', u'eggs'),
            (u'extends-cache', u'extends')
        ):
            directory = os.path.abspath(os.path.join(buildoutCache, directory))
            f.write(u'{} = {}\n'.format(directive, directory))
        f.write(u'[hosts]\n')
        f.write(u'public-address = {}\n'.format(hostname))
        f.write(u'[ports]\n')
        f.write(u'nginx = {}\n'.format(http))
        f.write(u'nginx-ssl = {}\n'.format(https))
        f.write(u'[supervisor]\n')
        f.write(u'username = {}\n'.format(superUser))
        f.write(u'password = {}\n'.format(superPassword))
        f.write(u'[tomcat]\n')
        f.write(u'username = {}\n'.format(tomcatUser))
        f.write(u'password = {}\n'.format(tomcatPassword))
        f.write(u'[zope]\n')
        f.write(u'username = {}\n'.format(zopeUser))
        f.write(u'password = {}\n'.format(zopePassword))
        f.write(u'[paths]\n')
        f.write(u'java = {}\n'.format(executables['java']))
        f.write(u'java_home = {}\n'.format(javaHome))
        f.write(u'nginx = {}\n'.format(executables['nginx']))
        f.write(u'varnishd = {}\n'.format(executables['varnishd']))
        f.write(u'extra = {}\n'.format(u':'.join(extraPaths)))
        if len(libdirs):
            f.write(u'libs = {}\n'.format(u':'.join(libdirs)))
        f.write(u'[users]\n')
        for i in (u'nginx', u'tomcat', u'varnish', u'zeo', u'zope'):
            f.write(u'{} = {}\n'.format(i, userID))

def _checkBuildoutCache(directory):
    logging.info(u'Checking buildout cache')
    def reportError(error):
        raise DeploymentError(u'Cannot access "{}" (errno: {})'.format(error.filename, error.strerror))
    logging.debug(u'Traversing all files/dirs under %s for writeability', directory)
    for root, dirs, files in os.walk(directory, onerror=reportError):
        for d in dirs:
            d = os.path.abspath(os.path.join(root, d))
            if not os.access(d, os.R_OK | os.X_OK | os.W_OK):
                raise DeploymentError(u'Cannot read, write, and traverse "{}"'.format(d))
        for f in files:
            f = os.path.abspath(os.path.join(root, f))
            if not os.access(f, os.R_OK | os.W_OK):
                raise DeploymentError(u'Cannot read and write "{}"'.format(f))
    for d in ('eggs', 'downloads', 'extends'):
        d = os.path.abspath(os.path.join(directory, d))
        logging.debug(u'Checking if %s is a directory', d)
        if not os.path.isdir(d):
            logging.debug(u'Creating %s', d)
            os.makedirs(d)

def _getCredentials(kind, options):
    username = getattr(options, u'{}_user'.format(kind))
    passwd = getattr(options, u'{}_password'.format(kind), None)
    if passwd is None:
        chars = string.letters + string.digits
        passwd = ''.join([random.choice(chars) for i in range(20)])
    return username, passwd

def _execAndLog(args):
    logging.debug(u'>>> %r', args)
    sub = subprocess.Popen(args, bufsize=1, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        close_fds=True, universal_newlines=True)
    output, error = sub.communicate()
    sub.wait()
    for line in output.split('\n'):
        logging.debug(u'... %s', line)
    if sub.returncode != 0:
        raise DeploymentError(u'Subprocess call failed with return code {} (command was {})'.format(sub.returncode,
            repr(args)))

def _bootstrap():
    logging.info(u'Bootstrapping the buildout')
    args = [
        os.path.join(u'python2.7', u'bin', u'python2.7'),
        u'bootstrap.py',
        u'--buildout-version={}'.format(_buildoutVersion),
        u'--setuptools-version={}'.format(_setupToolsVersion),
        '-c',
        u'site.cfg'
    ]
    _execAndLog(args)

def _buildout():
    logging.info(u'Building out; this can take a long time')
    args = [os.path.join(u'bin', u'buildout'), u'-c', u'site.cfg']
    _execAndLog(args)

def _checkSite(directory):
    logging.info(u'Checking old IPDA site at "%s"', directory)
    var = os.path.abspath(os.path.join(directory, u'var'))
    database = os.path.join(var, u'filestorage', u'Data.fs')
    logging.debug(u'Testing if database file %s exists', database)
    if not os.path.isfile(database):
        raise DeploymentError(u'Existing site at "{}" lacks a database at "{}"'.format(directory, database))
    blobs = os.path.join(var, u'blobstorage')
    logging.debug(u'Testing if blob directory %s exists', blobs)
    if not os.path.isdir(blobs):
        raise DeploymentError(u'Existing site at "{}" lacks blobstorage at "{}"'.format(directory, blobs))

def _copyContent(directory):
    logging.info(u'Copying content from existing IPDA site at "%s"', directory)
    var = os.path.abspath(os.path.join(directory, u'var'))
    database = os.path.join(var, u'filestorage', u'Data.fs')
    targetDir = os.path.abspath(os.path.join(u'var', u'filestorage'))
    if not os.path.isdir(targetDir):
        logging.debug(u'Creating directory %s', directory)
        os.makedirs(targetDir)
    logging.debug(u'Copying %s to %s', database, targetDir)
    shutil.copy(database, targetDir)
    blobs = os.path.join(var, u'blobstorage')
    targetDir = os.path.abspath(os.path.join(u'var', u'blobstorage'))
    if os.path.isdir(targetDir):
        logging.debug(u'Removing directory %s', targetDir)
        shutil.rmtree(targetDir)
    logging.debug(u'Copying tree %s to var', blobs)
    shutil.copytree(blobs, os.path.abspath(u'var/blobstorage'))
    registryDir = os.path.abspath(os.path.join(u'var', u'registry'))
    if os.path.isdir(registryDir):
        logging.debug(u'Removing barebones registry db at %s', registryDir)
        shutil.rmtree(registryDir)
    registryDB = os.path.join(var, u'registry')
    logging.debug(u'Copying tree %s to var', registryDB)
    shutil.copytree(registryDB, os.path.abspath(u'var/registry'))

def _deployEmptySite():
    logging.info(u'Deploying IPDA website with minimal content')
    args = [os.path.join(u'bin', u'buildout'), u'-c', u'site.cfg', 'install', 'basic-site']
    _execAndLog(args)

def _upgradeSite(user, password):
    logging.info(u'Setting up new Zope user and upgrading site')
    args = [os.path.join(u'bin', u'zope-debug'), u'run', os.path.join(u'support', u'upgrade.py'), user, password]
    _execAndLog(args)

def main(argv):
    _setupLogging()
    _checkCWD()
    parser = _getArgParser()
    ns = parser.parse_args(argv[1:])
    if ns.existing:
        _checkSite(ns.existing)
    executables = _findExecutables(ns)
    _checkVarnish(executables['varnishd'])
    libdirs = _checkLibraries(ns)
    extraPaths = set()
    for path in (executables['lynx'], executables['pdftohtml'], executables['wvHtml']):
        directory = os.path.dirname(path)
        extraPaths.add(directory)
    logging.debug(u'Extra PATH to set: %s', extraPaths)
    userID = _getUserID()
    logging.info(u'Processes will run with user ID "%s"', userID)
    _checkBuildoutCache(ns.buildout_cache)
    _installVirtualEnv(executables['python'])
    superUser, superPassword = _getCredentials(u'supervisor', ns)
    tomcatUser, tomcatPassword = _getCredentials(u'tomcat', ns)
    zopeUser, zopePassword = _getCredentials(u'zope', ns)
    _installSiteConfig(executables, extraPaths, libdirs, superUser, superPassword, tomcatUser, tomcatPassword,
        zopeUser, zopePassword, ns.public_hostname, ns.http_port, ns.https_port, userID, ns.buildout_cache)
    _bootstrap()
    _buildout()
    if ns.existing:
        _copyContent(ns.existing)
        _upgradeSite(zopeUser, zopePassword)
    else:
        _deployEmptySite()
    return True

if __name__ == '__main__':
    sys.exit(0 if main(sys.argv) else -1)
