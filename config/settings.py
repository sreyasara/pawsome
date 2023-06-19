from dotenv import load_dotenv
import os

load_dotenv(".env")
settings = os.getenv('SETTINGS')
debug = os.getenv('DEBUG')

if settings == "prod":
    print("PRODUCTION SERVER")
    DEBUG = False
    from .common_settings import *

    ALLOWED_HOSTS = ["dev.inbam.tech", ""]
    cors_allowed_origins = ["https://dev.inbam.tech", "http://dev.inbam.tech"]
    CSRF_TRUSTED_ORIGINS = ["https://dev.inbam.tech"]
    DEPLOYMENT_URL = "https://dev.inbam.tech"
    STATIC_ROOT = "/var/www/html/static/"
    MEDIA_ROOT = '/var/www/html/media'

else:
    print("DEV SERVER")
    DEBUG = True
    from .common_settings import *

    ALLOWED_HOSTS += ["dev.inbam.tech", ""]
    cors_allowed_origins += ["https://dev.inbam.tech", "http://dev.inbam.tech"]
    CSRF_TRUSTED_ORIGINS += ["http://dev.inbam.tech", "https://dev.inbam.tech"]

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            
        }
    }
