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
    "bootstrap4",
    "reporting",
    "userdb",
    "home",
    "discourse",
    "openstack",
    "django_slack",
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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
MESSAGE_TAGS = {messages.INFO: "primary", messages.ERROR: "danger"}


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


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATIC_ROOT = os.path.join(BASE_DIR, "../static")
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


# django-phonenumber-field settings

PHONENUMBER_DEFAULT_REGION = "GB"


# django-bootstrap settings

bootstrap4 = {
    # The URL to the jQuery JavaScript file
    "jquery_url": "//code.jquery.com/jquery.min.js",
    # The Bootstrap base URL
    "base_url": "//maxcdn.bootstrapcdn.com/bootstrap/3.3.6/",
    # Label class to use in horizontal forms
    "horizontal_label_class": "col-md-3",
    # Field class to use in horizontal forms
    "horizontal_field_class": "col-md-9",
    # Set HTML required attribute on required fields
    "set_required": True,
    # Set HTML disabled attribute on disabled fields
    "set_disabled": False,
    # Set placeholder attributes to label if no placeholder is provided
    "set_placeholder": False,
    # Class to indicate required (better to set this in your Django form)
    "required_css_class": "",
    # Class to indicate error (better to set this in your Django form)
    "error_css_class": "has-error",
    # Class to indicate success, meaning the field has valid input (better to set this in your Django form)
    "success_css_class": "has-success",
    # Renderers (only set these if you have studied the source and understand the inner workings)
    "formset_renderers": {"default": "bootstrap4.renderers.FormsetRenderer"},
    "form_renderers": {"default": "bootstrap4.renderers.FormRenderer"},
    "field_renderers": {
        "default": "bootstrap4.renderers.FieldRenderer",
        "inline": "bootstrap4.renderers.InlineFieldRenderer",
    },
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

try:
    from .locals import *  # noqa: F401,F403
except ImportError:
    pass

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
