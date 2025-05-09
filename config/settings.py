from pathlib import Path

import tomli

# ----------------------------------------------------------------------
# 0. SETUP
# ----------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

with open(BASE_DIR / "env.toml", mode="rb") as env_file:
    env = tomli.load(env_file)


# ----------------------------------------------------------------------
# 1. DJANGO CORE SETTINGS
# ----------------------------------------------------------------------

# DEBUGGING

DEBUG = env["core"]["debug"]

# CORE

ALLOWED_HOSTS = env["core"]["allowed_hosts"]

ADMINS = [("neftali", "neftalihrramos03@gmail.com")]

SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 60 * 60 * 24

USE_X_FORWARDED_HOST = True

# SECURITY

SECRET_KEY = env["core"]["secret_key"]

# MODELS

INSTALLED_APPS = [
    "apps.core",
    "widget_tweaks",
    "django_htmx",
    "django_linear_migrations",
    "rest_framework",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "rest_framework.authtoken",
    "import_export",
    "django.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
]

# HTTP

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "common.middleware.LoginRequiredMiddleware",
    "common.dx_django_base.log_request.LogRequestMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "common.middleware.TempPasswordMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

WSGI_APPLICATION = "config.wsgi.application"

# URLs

ROOT_URLCONF = "config.urls"

# TEMPLATES

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                # "common.context_processors.sidebar",
                # "common.context_processors.custom_data",
            ],
        },
    },
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# DATABASES

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env["database"]["name"],
        "USER": env["database"]["user"],
        "PASSWORD": env["database"]["password"],
        "HOST": env["database"]["host"],
        "PORT": env["database"]["port"],
    }
}

# INTERNATIONALIZATION

LANGUAGE_CODE = "en-us"

LANGUAGES = [
    ("en-us", "English"),
    ("es", "Spanish"),
]

USE_I18N = True

USE_THOUSAND_SEPARATOR = True

TIME_ZONE = "America/El_Salvador"

USE_TZ = True

# FILE UPLOADS

MEDIA_URL = "media/"

MEDIA_ROOT = env["storage"]["media_root"]
MEDIA_LOCAL = "local"
MEDIA_TMP = "tmp"

# LOGGING

if logging_root := env["logging"]["logging_root"]:
    LOGGING_ROOT = Path(env["logging"]["logging_root"])
else:
    LOGGING_ROOT = BASE_DIR / "logs"

# OTHERS

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ----------------------------------------------------------------------
# 2. DJANGO CONTRIB SETTINGS
# ----------------------------------------------------------------------

# AUTH

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"django.contrib.auth.password_validation.{validator}"}
    for validator in (
        "UserAttributeSimilarityValidator",
        "MinimumLengthValidator",
        "CommonPasswordValidator",
        "NumericPasswordValidator",
    )
]

AUTH_USER_MODEL = "core.User"

LOGIN_URL = "/auth/login/"

LOGIN_REDIRECT_URL = "/"

LOGOUT_REDIRECT_URL = LOGIN_URL

# STATIC FILES

STATICFILES_DIRS = [BASE_DIR / "static"]

STATIC_URL = "static/"

STATIC_ROOT = env["storage"]["static_root"] or None

# ----------------------------------------------------------------------
# 3. THIRD PARTY APPS SETTINGS
# ----------------------------------------------------------------------

# DJANGO DEBUG TOOLBAR

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)

    DEBUG_TOOLBAR_CONFIG = {
        "ROOT_TAG_EXTRA_ATTRS": "hx-preserve",
        "INTERCEPT_REDIRECTS": False,
    }


# ----------------------------------------------------------------------
# 4. PROJECT SETTINGS
# ----------------------------------------------------------------------

BOT_USERNAME = "ov"

ALLOWED_USER_EMAIL_DOMAINS = ["gmail.com", "hotmail.com"]

PASSWORD_HISTORY = 5
