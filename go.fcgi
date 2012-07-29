#!/sparc_soft/www.dam/htdocs/scicomp/pool/bin/python
import sys, os

# Add a custom Python path.
sys.path.insert(0, "/sparc_soft/www.dam/htdocs/scicomp")
sys.path.insert(0, "/sparc_soft/www.dam/htdocs/scicomp/scg")

# Switch to the directory of your project. (Optional.)
# os.chdir("/home/user/myproject")

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "scg.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="prefork", daemonize="false", maxchildren=1)
