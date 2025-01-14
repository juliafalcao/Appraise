#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Appraise.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    
    if sys.argv[1] == "runserver":
        # load dev config into env
        from configparser import ConfigParser

        cfg = ConfigParser()
        cfg.read("config.ini")
        assert len(cfg), "Config was not loaded correctly"
        
        for key, val in cfg["dev"].items():
            os.environ[key.upper()] = val

    execute_from_command_line(sys.argv)
