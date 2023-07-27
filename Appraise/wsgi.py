"""
WSGI config for Appraise project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Appraise.settings")

# load configs into env
from configparser import ConfigParser
cfg = ConfigParser()
cfg.read("/var/www/rival/public_html/translation-eval/config.ini")
assert len(cfg), "Config was not loaded correctly"

for key, val in cfg["prod"].items():
    os.environ[key.upper()] = val

application = get_wsgi_application()  # pylint: disable=invalid-name
