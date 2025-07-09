from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# --------------------
# Security Settings
# --------------------

SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
DEBUG = os.getenv("DEBUG", "False") == "True"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# --------------------
# Installed Apps
# --------------------

INSTALLED_APPS = [
    'tcs',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# --------------------
# Middleware
# --------------------

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',  # must be at the top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --------------------
# URL & WSGI
# --------------------

ROOT_URLCONF = 'tcms.urls'
WSGI_APPLICATION = 'tcms.wsgi.application'

# --------------------
# Templates
# --------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # your custom templates
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

# --------------------
# Database
# --------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv("DB_NAME", "tcms"),
        'USER': os.getenv("DB_USER", "root"),
        'PASSWORD': os.getenv("DB_PASSWORD", ""),
        'HOST': os.getenv("DB_HOST", "localhost"),
        'PORT': os.getenv("DB_PORT", "3306"),
    }
}

# --------------------
# Authentication
# --------------------

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = ''
LOGOUT_REDIRECT_URL = '/login/'

# --------------------
# Internationalization
# --------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --------------------
# Static Files (CSS, JS)
# --------------------

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'templates', 'tcs_temp', 'assets'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --------------------
# Media Files (Uploads)
# --------------------

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'Testcases')

# --------------------
# Default Primary Key Field Type
# --------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
