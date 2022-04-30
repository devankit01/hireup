import os

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%4*n=7m-59$ek76-qr9^tg(#r-0!08+qa9-6f+j68j&rf$7mkf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'HireApp',
    'UserApp',
    'NotesApp',
    'ckeditor',
    'django_s3_sqlite',
    'channels',
    'chatapp',
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

ROOT_URLCONF = 'MainApp.urls'

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

WSGI_APPLICATION = 'MainApp.wsgi.application'
ASGI_APPLICATION = 'MainApp.asgi.application'


AWS_S3_ENDPOINT_URL = 'https://s3.amazonaws.com'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_REGION_NAME = 'ap-south-1'
AWS_ACCESS_KEY_ID = 'AKIAXLSZRNQVPA26ZV4D'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'hireup-project'
AWS_DEFAULT_ACL = None

# DATABASES = {
#     "default": {
#         "ENGINE": "django_s3_sqlite",
#         "NAME": "db.sqlite3",
#         "BUCKET": "hireup-project",
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Email Setup
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'hireup.contact@gmail.com'
EMAIL_HOST_PASSWORD = 'Ankit@98'

# CLOUDWATCH_AWS_ID = 'AKIAXLSZRNQVFTPJ5KJE'
# CLOUDWATCH_AWS_KEY = 'a8YluunadlTqL57YivRpHBNgFWgPdmiBFerhHx/N'
# AWS_DEFAULT_REGION = 'us-east-1'  # Be sure to update with your AWS region


# AWS_REGION_NAME = "us-east-1"
# import boto3
# boto3_logs_client = boto3.client("logs", region_name=AWS_REGION_NAME)

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'root': {
#         'level': 'DEBUG',
#         'handlers': ['watchtower', 'console'],
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#         'watchtower': {
#             'class': 'watchtower.CloudWatchLogHandler',
#             'boto3_client': boto3_logs_client,
#             'log_group_name': 'Hire_App',
#             'level': 'DEBUG',
#         }
#     },
#     'loggers': {
#         'django': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#             'propagate': False
#         }
#         # Add any other logger-specific configuration here.
#     }
# }

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}
