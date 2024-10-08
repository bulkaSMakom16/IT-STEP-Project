import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

GOOGLE_OAUTH_CLIENT_ID = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
if not GOOGLE_OAUTH_CLIENT_ID:
    raise ValueError(
        'GOOGLE_OAUTH_CLIENT_ID is missing.' 
        'Have you put it in a file at core/.env ?'
    )

GOOGLE_OAUTH_CLIENT_SECRET = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')

if not GOOGLE_OAUTH_CLIENT_ID or not GOOGLE_OAUTH_CLIENT_SECRET:
    raise ValueError(
        'Google OAuth credentials are missing. '
        'Ensure you have GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET in your core/.env file.'
    )

# We need these lines below to allow the Google sign in popup to work.
SECURE_REFERRER_POLICY = 'no-referrer-when-downgrade'
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin-allow-popups"


from pathlib import Path
import os
import requests
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-o^zgyr&r^4y^(np1uv0e0wq=0zhd)lxsxhe!@*2x!u7qwq%75o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


LOGOUT_REDIRECT_URL = 'index'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]


SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

ROOT_URLCONF = 'itstep.urls'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

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
                'web.context_processors.cart',
                'web.context_processors.cart_count',
            ],
        },
    },
]


WSGI_APPLICATION = 'itstep.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SOCIALACCOUT_PROVIDERS = {
    'google':{
        'APP':{
            'client_id': '471812366920-lalkqqmgrir4022etjijjkeoh532adoc.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    }
}