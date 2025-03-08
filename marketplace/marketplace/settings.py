"""
Django settings for marketplace project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
import logging
from pathlib import Path
import cloudinary_storage

logger = logging.getLogger(__name__)

from dotenv import load_dotenv
# import dj_database_url
# from urllib.parse import quote_plus
# python marketplace/manage.py runserver 0.0.0.0:$PORT

load_dotenv()

logger.info('here are the environment variables')
for k in os.environ:
    logger.info(f"{k}={os.environ[k]}")
logger.info('end')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DEBUG", False))

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(' ')
CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS=os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://localhost').split(' ')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    'core',
    'vender_center',
    'crispy_forms',
    "crispy_tailwind",
    'cloudinary',
    'cloudinary_storage',
    
]


CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'marketplace.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'marketplace.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases



# DATABASES = {
#     'default': dj_database_url.config(
#         default=os.environ.get('DATABASE_URL'),
#         conn_max_age=600
#     )
# }

# DB_URL = os.environ.get('DATABASE_URL')
# if DB_URL:
#     DB_URL = DB_URL.replace('postgres://', 'postgresql://', 1)
#     DATABASES = {
#         'default': dj_database_url.parse(DB_URL)
#     }
# else:
DATABASES = {
    'default': {
        'ENGINE': os.environ.get("DB_ENGINE", "django.db.backends.postgresql"),
        'NAME': os.environ.get("DB_NAME",'eshoppydb'),
        'USER': os.environ.get("DB_USER",'store_user'),
        'PASSWORD': os.environ.get("DB_PASSWORD",'Admin333'),
        'HOST': os.environ.get("DB_HOST",'localhost'),
        'PORT': os.environ.get("DB_PORT",'5432'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOGIN_URL = 'login'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIR = [
    os.path.join(BASE_DIR, 'static')
]
MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET')
}
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
