"""
Located under app/
"""

import os

from django.apps import apps
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VirtualClassroom.src.settings")
apps.populate(settings.INSTALLED_APPS)