"""
WSGI config for ehf project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os,sys
sys.path.append('/var/www/html/')
sys.path.append('/var/www/html/ehfpi')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ehf.settings")

# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()

import django.core.handlers.wsgi
_application = django.core.handlers.wsgi.WSGIHandler()
def application(environ, start_response):
    return _application(environ, start_response)
