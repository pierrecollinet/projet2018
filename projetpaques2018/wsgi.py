"""
WSGI config for projetpaques2018 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys



from django.core.wsgi import get_wsgi_application

import settings
# To accept accent
if settings.DEBUG :
  reload(sys)
  sys.setdefaultencoding("utf-8")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projetpaques2018.settings")
application = get_wsgi_application()
