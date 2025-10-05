import os, re
from pathlib import Path
from decouple import config, Csv
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET', 'django-insecure-brx^g3f$ahjhpq9k#2zwy(5u6%un4lj(@-3u@&_x#^kg_%a7lw') #'django-insecure-brx^g3f$ahjhpq9k#2zwy(5u6%un4lj(@-3u@&_x#^kg_%a7lw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'accounts',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'home',
    'events',
    'memberships',
    'dashboard',
    
    'tailwind',
    'theme',
    'tinymce',
    
]

AUTH_USER_MODEL = 'accounts.Account'
AUTHENTICATION_BACKENDS = ['accounts.utilities.backends.EmailBackend']
LOGIN_URL = 'accounts:login'


TAILWIND_APP_NAME = 'theme'
NPM_BIN_PATH = "npm.cmd"
INTERNAL_IPS = [
    "127.0.0.1", '0.0.0.0'
]

TINYMCE_DEFAULT_CONFIG = {
    'content_style': '* { margin: 0 !important; padding: 0 !important; }',
    'theme_advanced_fonts': 'DM Sans=dm-sans,Arial=arial,helvetica,sans-serif',
    'height': "400px",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    # 'selector': 'textarea',
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap print preview anchor searchreplace visualblocks fullscreen insertdatetime media table paste help",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | a11ycheck ltr rtl | showcomments addcomment",
}

PASSWORD_RESET_TIMEOUT = 14400

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880 # 5MB

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ctblackpros.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ctblackpros.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Johannesburg'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

if DEBUG:
    ALLOWED_HOSTS = []
    X_FRAME_OPTIONS = "SAMEORIGIN"
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    
    STATIC_URL = 'static/'
    STATICFILES_DIRS = [
        BASE_DIR / 'static'
    ]
    STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
    
else:
    ALLOWED_HOSTS = ['ctblackpros.co.za', 'www.ctblackpros.co.za', 'localhost']
    CSRF_TRUSTED_ORIGINS = ['https://127.0.0.1', 'https://localhost', 'https://ctblackpros.co.za', 'https://www.ctblackpros.co.za']
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    X_FRAME_OPTIONS = "SAMEORIGIN"
    

    # SSL SETTINGS
    
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config("DB_NAME"),
            'USER': config("DB_USER"),
            'PASSWORD': config("DB_PASSWORD"),
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    
    
    
    STATIC_URL = 'static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    
    SILENCED_SYSTEM_CHECKS = ['security.W019']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.ctblackpros.co.za'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@ctblackpros.co.za'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = 'noreply@ctblackpros.co.za'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
