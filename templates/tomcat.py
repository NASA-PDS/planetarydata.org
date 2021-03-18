#!${buildout:executable}
#
# Tomcat run script.  Generated from templates/tomcat.py.
# Edit that, not this.  Unless of course, this *is* that.  Then edit this.
#
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

import os, os.path, signal, subprocess, sys

# These values are set by collective.recipe.template (in addition to the shebang at the top):
home, tomcat, java_home = '${buildout:directory}', '${tomcat:location}', '${paths:java_home}'

# Derived values
dbDir = os.path.join(home, 'var')
tomcatBin = os.path.join(tomcat, 'bin')
tomcatStart, tomcatStop = os.path.join(tomcatBin, 'startup.sh'), os.path.join(tomcatBin, 'shutdown.sh')
logFile = os.path.join(dbDir, 'log', 'catalina.out')

# Make DB dir
if not os.path.isdir(dbDir):
    os.makedirs(dbDir)
opts = os.environ.get('CATALINA_OPTS', '')
opts += ' -Dderby.system.home="%s"' % dbDir
os.environ['CATALINA_OPTS'] = opts
os.environ['JAVA_HOME'] = java_home
os.environ['CATALINA_OUT'] = logFile

# Handle termination signals
def stopTomcat(signum, frame):
    subprocess.check_call(tomcatStop, stderr=subprocess.STDOUT)
    sys.exit(0)
for sig in (signal.SIGHUP, signal.SIGINT, signal.SIGQUIT, signal.SIGTERM):
    signal.signal(sig, stopTomcat)

# Start er up and we're done til termination signal comes in
subprocess.check_call(tomcatStart, stderr=subprocess.STDOUT)
signal.pause()

# We should never get here, but just in case
stopTomcat()
