
import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv(BASE_DIR / '.env')



SECRET_KEY = os.environ.get(
    'SECRET_KEY',
)


DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    h.strip()
    for h in os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
    if h.strip()
]

CSRF_TRUSTED_ORIGINS = [
    o.strip()
    for o in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
    if o.strip()
]

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'anymail',

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



DATABASES = {
    'default': {

        'ENGINE': os.environ.get('DB_ENGINE') or 'django.db.backends.sqlite3',
        'NAME': os.environ.get('DB_NAME') or str(BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', ''),
    }
}




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




LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Sofia'

USE_I18N = True

USE_TZ = True




STATIC_URL = 'static/'

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "mediafiles"

STATIC_ROOT = BASE_DIR / 'staticfiles_collected'

STATICFILES_DIRS = [
    BASE_DIR / 'staticfiles',
]



AWS_ACCESS_KEY_ID = os.environ.get('R2_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('R2_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('R2_BUCKET_NAME', '')

AWS_S3_ENDPOINT_URL = os.environ.get('R2_ENDPOINT_URL', '')

AWS_S3_CUSTOM_DOMAIN = os.environ.get('R2_PUBLIC_DOMAIN', '')
AWS_S3_ADDRESSING_STYLE = 'virtual'
AWS_QUERYSTRING_AUTH = False
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



EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'

RESEND_API_KEY = os.environ.get('RESEND_API_KEY', '')

RESEND_FROM_EMAIL = os.environ.get('RESEND_FROM_EMAIL', 'onboarding@resend.dev')

if RESEND_API_KEY:
    EMAIL_BACKEND = 'anymail.backends.resend.EmailBackend'
    ANYMAIL = {'RESEND_API_KEY': RESEND_API_KEY}
    # This is the "From" address SiteSettings/EmailMessage build on top of
    # (see ContactsView.post) — must be Resend's own verified sender, not
    # the business's Gmail address, which Resend doesn't own/can't send as.
    DEFAULT_FROM_EMAIL = RESEND_FROM_EMAIL
elif EMAIL_HOST_USER:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'noreply@example.com'

# Fallback recipient if SiteSettings.email is empty in the admin.
DEFAULT_CONTACT_EMAIL = os.environ.get('DEFAULT_CONTACT_EMAIL', EMAIL_HOST_USER)