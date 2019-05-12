"""
Django settings for library project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import bootstrapform_jinja
from django.contrib.messages import constants as messages
from urllib.parse import urlparse
import dj_database_url

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.DEBUG: 'info',
}

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2d&%w61wuc$!$%r6pq$3=c4w+uqb)10x_5%2(_vh_4td5*f%_l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '.kdhx.org', '104.248.237.137', 'kdhxlib.chrisbay.net']


# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'albums',
    'classification',
    'data',
    'profiles',
    'social_django',
    'django_jinja',
    'bootstrapform_jinja',
    'django_extensions',
    'reversion',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'library.middleware.LoginRequiredMiddleware',
    'library.middleware.CatchOperationalError',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

ROOT_URLCONF = 'library.urls'

# TODO - Consider removing context_processors from jinja2 backends
# per the rec at https://docs.djangoproject.com/en/1.11/topics/templates/
TEMPLATES = [
    {
        'NAME': 'site_templates',
        'BACKEND': 'django_jinja.backend.Jinja2',
        'APP_DIRS': True,
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'OPTIONS': {
            'match_extension': '.jinja',
            'app_dirname': 'templates',
            'environment': 'library.jinja2.environment',
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'profiles.context_processors.login_url',
            ]
        },
    },
    {
        'NAME': 'bootstrapform_templates',
        'BACKEND': 'django_jinja.backend.Jinja2',
        'DIRS': [
            os.path.join(os.path.dirname(bootstrapform_jinja.__file__),
                         'templates')
        ],
        'OPTIONS': {
            'match_extension': '.jinja',
            'environment': 'library.jinja2.environment',
        },
    },
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'library.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

if os.environ.get('ENVIRONMENT') == 'DEVELOPMENT':
    psql_ssl_require = False
else:
    psql_ssl_require = True

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=psql_ssl_require)
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'UserAttributeSimilarityValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'MinimumLengthValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'CommonPasswordValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'NumericPasswordValidator'),
    },
]

AUTH_USER_MODEL = 'profiles.LibraryUser'

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Django Social Auth Config

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = '/login/google-oauth2/'
LOGIN_ERROR_URL = '/login-error/'
HOME_URL = '/albums/'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ['ORG_KDHX_LIBRARY_OAUTH2_CLIENT']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ['ORG_KDHX_LIBRARY_OAUTH2_SECRET']
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ['kdhx.org']

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/albums'

LOGIN_EXEMPT_URLS = [
    '',
    LOGIN_ERROR_URL.lstrip('/'),
    'complete/google-oauth2/',
    'admin/*',
    'albums/',
    'albums/detail/',
]
