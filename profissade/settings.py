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

ALLOWED_HOSTS = ['*']

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_APPS = [
        'rest_framework',
        'raven.contrib.django.raven_compat',
        'simple_email_confirmation',
        'anymail',
        'social_django',
        'mptt',
        'widget_tweaks',
        'storages',
        ]

MAIN_APPS = [
        'profissade',
        'accounts',
        'core',
        'business',
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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# auth

AUTH_USER_MODEL = 'accounts.User'

LOGIN_REDIRECT_URL = '/conta/perfil/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/usuario/identifique-se/'

SESSION_COOKIE_DOMAIN = config('SESSION_COOKIE_DOMAIN')
SESSION_COOKIE_PORT = config('SESSION_COOKIE_PORT')

USER_FIELDS = ['email']
SOCIAL_AUTH_FACEBOOK_KEY = config('FACEBOOK_APP_ID')
SOCIAL_AUTH_FACEBOOK_SECRET = config('FACEBOOK_APP_SECRET')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'cover, name, first_name, last_name, age_range,'
    'link, gender, locale, picture'}


AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        'social_core.backends.facebook.FacebookOAuth2',
        ]

SOCIAL_AUTH_PIPELINE = (
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.auth_allowed',
        'social_core.pipeline.social_auth.social_user',
        'social_core.pipeline.user.get_username',
        'social_core.pipeline.user.create_user',
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
        'social_core.pipeline.social_auth.associate_by_email',
        )

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
AWS_STORAGE_BUCKET_NAME = "profissade"
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL
#STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(PROJECT_DIR, 'static/')]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

ANYMAIL = {
        "MAILGUN_API_KEY": os.environ.get('MAILGUN_API_KEY'),
        "MAILGUN_SENDER_DOMAIN": os.environ.get('MAILGUN_SENDER_DOMAIN'),
        }

EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"
DEFAULT_CC_EMAIL = 'no-reply@profissa.de'

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
