"""
WSGI config for omnisolace project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omnisolace.settings')

application = get_wsgi_application()
