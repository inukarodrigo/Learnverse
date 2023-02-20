"""
WSGI config for src project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VirtualClassroom.src.settings')

application = get_wsgi_application()

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.settings")
#os.environ['DJANGO_SETTINGS_MODULE'] = 'src.settings' , settings.configure()
