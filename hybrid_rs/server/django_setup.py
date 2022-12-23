import os
from typing import List

from django import template
from django.conf import settings
from django.utils.crypto import get_random_string

from hybrid_rs.server.config import config


BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
STATIC_URL: str = '/static/'
STATICFILES_DIRS: List[str] = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT: str = os.path.join(BASE_DIR, "static_root")

# This is a module to setup url patterns
ROOT_URLCONF: str = 'hybrid_rs.server.url_setup'


def setup() -> None:
    settings.configure(
        DEBUG=config['DEBUG'],
        # Disable host header validation
        ALLOWED_HOSTS=["*"],
        # Make this module the urlconf
        ROOT_URLCONF=ROOT_URLCONF,
        # We aren't using any security features but Django requires this setting
        SECRET_KEY=get_random_string(50),
        INSTALLED_APPS = [
            'django.contrib.staticfiles'
        ],
        TEMPLATES = [
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [os.path.join(BASE_DIR, 'templates')],
                "OPTIONS": {
                    "libraries": {
                        "tags": "hybrid_rs.server.templatetags.pagination_tags"
                    }
                }
            }
        ],
        STATIC_URL = STATIC_URL,
        STATICFILES_DIRS = STATICFILES_DIRS,
        STATIC_ROOT = STATIC_ROOT
    )
