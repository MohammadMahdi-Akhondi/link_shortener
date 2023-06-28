from .base import *


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql',
        'NAME':     os.environ.get('DB_NAME'),
        'USER':     os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST':     os.environ.get('DB_HOST'),
        'PORT':     os.environ.get('DB_PORT'),
    }
}

# Email configs
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = config('EMAIL_HOST')
EMAIL_PORT          = config('EMAIL_PORT')
EMAIL_HOST_USER     = config('EMAIL_HOST_USER')
DEFAULT_FROM_EMAIL  = config('DEFAULT_FROM_EMAIL')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS       = True

# static file configs
STATIC_ROOT = BASE_DIR / 'static/'
