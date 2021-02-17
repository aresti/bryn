"""
Django settings for brynweb project.
"""

import os

from django.contrib.messages import constants as messages

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

ALLOWED_HOSTS = []

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

ADMINS = [("Nick", "n.j.loman.bham.ac.uk")]
ADMIN_EMAIL = "Lisa.Marchioretto@quadram.ac.uk"
SERVER_EMAIL = "noreply@discourse.climb.ac.uk"
DEFAULT_FROM_EMAIL = "noreply@discourse.climb.ac.uk"

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "django_slack",
    "coverage",
    "rest_framework",
    "widget_tweaks",
    "core",
    "userdb",
    "home",
    "openstack",
    "reporting",
    "discourse",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "brynweb.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "frontend/build/templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "brynweb.wsgi.application"

# Custom message tags
MESSAGE_TAGS = {
    messages.ERROR: "is-danger",
    messages.INFO: "is-info",
    messages.SUCCESS: "is-success",
    messages.WARNING: "is-warning",
}


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Login settings

LOGIN_URL = "user:login"
LOGIN_REDIRECT_URL = "home:home"

# Don't reject auth where User.is_active is False; allows for custom error on email not-validated
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.AllowAllUsersModelBackend",
    "userdb.backends.UniqueEmailBackend",
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATIC_ROOT = os.path.join(BASE_DIR, "../static")
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "frontend/build/static"),
]


# django-phonenumber-field settings

PHONENUMBER_DEFAULT_REGION = "GB"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),
    "DEFAULT_THROTTLE_RATES": {"anon": "100/day", "user": "5000/day"},
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "console": {"level": "DEBUG", "class": "logging.StreamHandler"},
        "logfile": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": BASE_DIR + "/../logfile",
        },
        "slack_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django_slack.log.SlackExceptionHandler",
        },
    },
    "loggers": {"django": {"level": "ERROR", "handlers": ["slack_admins"]}},
    "root": {"level": "INFO", "handlers": ["console", "logfile"]},
}

SLACK_FAIL_SILENTLY = True
SLACK_BACKEND = "django_slack.backends.UrllibBackend"

# Local secrets

try:
    from .locals import *  # noqa: F401,F403
except ImportError:
    pass

# Hashids

HASHIDS = {"SALT": HASHIDS_SALT, "MIN_LENGTH": 11}  # noqa: F405

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
