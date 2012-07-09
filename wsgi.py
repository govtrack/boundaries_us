import os
import sys

os.chdir("/home/govtrack/boundaries_us")
sys.path.append(".")
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

