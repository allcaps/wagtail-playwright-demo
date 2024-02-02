from .base import *  # NOQA

# Never commit secret key to version control :P
SECRET_KEY = "not-so-secret-in-testing"

# https://docs.djangoproject.com/en/5.0/topics/async/#async-safety
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# `live_server` fails when ManifestFilesStorage is active.
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
STATIC_URL = "/static/"
STATIC_ROOT = "/static/"
