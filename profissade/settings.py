import os
# separete instance elements
from decouple import config
# database alternate
from dj_database_url import parse as dburl

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.join(BASE_DIR, 'profissade')

SECRET_KEY = config('SECRET_KEY')

# get debug on .env
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['teste.profissa.com.br', 'profissa.de']

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_APPS = [
        'rest_framework',
        'raven.contrib.django.raven_compat',
        'simple_email_confirmation',
        'anymail',
        'mptt',
        'widget_tweaks',
        'storages',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.facebook',
        ]

MAIN_APPS = [
        'profissade',
        'accounts',
        'core',
        'business',
        'presentations',
        'solicitations',
        ]

INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + MAIN_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'profissade.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(PROJECT_DIR, 'templates')
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'profissade.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

default_dburl = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
DATABASES = {
    'default': config(
        'DATABASE_URL', default=default_dburl, cast=dburl)
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        'NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Campo_Grande'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# auth

AUTH_USER_MODEL = 'accounts.User'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/usuario/identifique-se/'

SESSION_COOKIE_DOMAIN = config('SESSION_COOKIE_DOMAIN')
SESSION_COOKIE_PORT = config('SESSION_COOKIE_PORT')

USER_FIELDS = ['email']

AUTHENTICATION_BACKENDS = [
        'allauth.account.auth_backends.AuthenticationBackend',
        'accounts.backends.ModelBackend',
        'django.contrib.auth.backends.ModelBackend',
                ]

SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
       {'METHOD': 'oauth2',
        'SCOPE': ['email','public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time'],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'kr_KR',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.4'}}


#facebook
SOCIAL_AUTH_FACEBOOK_KEY = config('SOCIAL_AUTH_FACEBOOK_KEY')  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = config('SOCIAL_AUTH_FACEBOOK_SECRET') #app key

SOCIALACCOUNT_QUERY_EMAIL = True

SITE_ID = 1

ACCOUNT_EMAIL_REQUIRED=True
ACCOUNT_USERNAME_REQURIED=True


if DEBUG:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_DIRS = [os.path.join(PROJECT_DIR, 'static/')]
else:
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = 'profissade'
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_OBJECT_PARAMETERS = {
            'CacheControl': 'max-age=86400',
            }
    AWS_LOCATION = 'static'

    STATICFILES_DIRS = [
            os.path.join('profissade/static'),
            ]
    STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


"""
ANYMAIL = {
        "MAILGUN_API_KEY": config('MAILGUN_API_KEY'),
        "MAILGUN_SENDER_DOMAIN": config('MAILGUN_SENDER_DOMAIN'),
        }

EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
DEFAULT_CC_EMAIL = 'no-reply@profissa.de'
"""

EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'postmaster@mg.profissa.de'
EMAIL_HOST_PASSWORD= 'ea025707dabcf33cac6f0b9210e31440'
EMAIL_USE_TLS = True

# sentry
RAVEN_URL = os.environ.get('RAVEN_URL')

if RAVEN_URL:
    RAVEN_CONFIG = {'dsn': RAVEN_URL}
    ROOT_HANDLER = 'sentry'
else:
    RAVEN_CONFIG = {}
    ROOT_HANDLER = 'stderr'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': [ROOT_HANDLER],
    },
    'formatters': {
        'normal': {
            'format': '%(levelname)s %(name)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'stderr': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'normal',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.Sentry'
            'Handler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
        },
        'py.warnings': {
            'handlers': ['console'],
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['stderr'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['stderr'],
            'propagate': False,
        },
    }
}
