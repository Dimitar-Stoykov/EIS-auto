
import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Loads variables from .env (local, gitignored) into os.environ.
load_dotenv(BASE_DIR / '.env')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Falls back to this dev-only value if .env / SECRET_KEY env var isn't set.
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
)

# SECURITY WARNING: don't run with debug turned on in production!
# os.environ values are always strings, so "False" must be compared as text —
# otherwise DEBUG = "False" would be truthy and debug mode would stay on.
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
    if h.strip()
]

# Needed once the site sits behind HTTPS on a real domain — Django rejects
# POST requests (admin login, the contact form) whose Origin isn't listed
# here. Leave empty locally; set to e.g. "https://eisauto.com" in .env
# when deploying.
CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
    if o.strip()
]

# Site only has the admin login — send anyone Django would otherwise
# redirect to the default /accounts/login/ to /admin/login/ instead.
LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',

    'eis_project',
    'eis_project.eisauto.apps.EisautoConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'eis_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'eis_project.eisauto.context_processors.service_pages',
            ],
        },
    },
]

WSGI_APPLICATION = 'eis_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases
# Defaults to the local sqlite file (unchanged) if no DB_* env vars are set.
# Set these in .env to point at a real Postgres/MySQL server without
# touching this file (e.g. when deploying).

DATABASES = {
    'default': {
        # "or" (not .get's default=) on purpose: .env sets these keys to
        # empty strings when unused, and .get() only falls back when the
        # key is missing entirely, not when it's "" — "or" catches both.
        'ENGINE': os.environ.get('DB_ENGINE') or 'django.db.backends.sqlite3',
        'NAME': os.environ.get('DB_NAME') or str(BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', ''),
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Sofia'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "mediafiles"

# Required by `collectstatic` even though R2 (below) actually receives the
# files in production — this is just where Django's checks expect a path.
STATIC_ROOT = BASE_DIR / 'staticfiles_collected'

STATICFILES_DIRS = [
    BASE_DIR / 'staticfiles',
]


# Cloudflare R2 (S3-compatible) — static + media storage in production.
# Local dev is untouched: with these env vars unset, Django falls back to
# its normal local filesystem storage (staticfiles/ + mediafiles/), so nothing
# changes day-to-day unless you're actually deploying.
AWS_ACCESS_KEY_ID = os.environ.get('R2_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('R2_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('R2_BUCKET_NAME', '')
# e.g. https://<account_id>.r2.cloudflarestorage.com
AWS_S3_ENDPOINT_URL = os.environ.get('R2_ENDPOINT_URL', '')
# Public hostname files are served from — either R2's own pub-xxxx.r2.dev
# (fine for testing) or a real custom domain later. No scheme, no slash.
AWS_S3_CUSTOM_DOMAIN = os.environ.get('R2_PUBLIC_DOMAIN', '')
AWS_S3_ADDRESSING_STYLE = 'virtual'
AWS_QUERYSTRING_AUTH = False  # public bucket — no signed/expiring URLs
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_FILE_OVERWRITE = False

USE_R2 = bool(
    AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
    and AWS_STORAGE_BUCKET_NAME and AWS_S3_ENDPOINT_URL
)

if USE_R2:
    STORAGES = {
        "default": {"BACKEND": "eis_project.storage_backends.MediaStorage"},
        "staticfiles": {"BACKEND": "eis_project.storage_backends.StaticStorage"},
    }


# Email (contact form on /contacts + admin password reset)
# Values come from .env (see .env.example). Without EMAIL_HOST_USER set,
# emails just print to the console — useful for local testing without
# real credentials.
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

EMAIL_BACKEND = (
    'django.core.mail.backends.smtp.EmailBackend'
    if EMAIL_HOST_USER
    else 'django.core.mail.backends.console.EmailBackend'
)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'

# Sent as the "From" address (most SMTP providers reject a spoofed visitor
# email as From); the visitor's email is set as Reply-To instead.
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER or 'noreply@example.com'

# Fallback recipient if SiteSettings.email is empty in the admin.
DEFAULT_CONTACT_EMAIL = os.environ.get('DEFAULT_CONTACT_EMAIL', EMAIL_HOST_USER)