"""
Django settings for YoYoProject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MEDIA_ROOT = 'G:/py_work_space/IMG_DATA/'
MEDIA_URL = '/imgs/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9#c*k5wv*zv#b=fz=!qim8v$ondn&2tertc#)_3^52=xlh6$xy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ws4redis',
    'rest_framework',
    'yyUserCenter',
    'yyStaffManager',
    'yyImgManager',
    'yyFriendshipManager',
    'yyMongoImgManager',
    'yyTagManager',
    'yyCRM',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware', 

    #'django.middleware.transaction.TransactionMiddleware',
)



ROOT_URLCONF = 'YoYoProject.urls'

WSGI_APPLICATION = 'YoYoProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yy_db',
        'USER': 'root',  
        'PASSWORD': '111111',  
        'HOST': '127.0.0.1',  
        'PORT': '3306', 
    }
}


#logging setting
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
     'formatters': {
    'standard': {
                     'format': '%(levelname)s %(asctime)s %(message)s'
                },
     },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR + '/logs/','yy.log'),
        },
    },
           
    
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

#session settings
SESSION_COOKIE_AGE=60*30 #30 minutes


#Cache settings
CACHES = {
    "default": {
        "BACKEND": "redis_cache.cache.RedisCache",
        "LOCATION": "121.41.46.183:6379:1",
        "OPTIONS": {
            "CLIENT_CLASS": "redis_cache.client.DefaultClient",
            
        }
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = 'G:/py_work_space/YoYoProject/static'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    'G:/py_work_space/YoYoProject/'
)


