"""
Django settings for webbase project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import datetime
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-n919u-1x#hdb8aaf$qba6+9-+@mla*ofaz81#mc6z2q)-=18%&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ["*"]
ALLOWED_HOSTS = ["125.25.57.91", "edi-vcst.in.th","https://edi-vcst.in.th"]
CSRF_TRUSTED_ORIGINS =  ["125.25.57.91", "edi-vcst.in.th","https://edi-vcst.in.th"]

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    # 'grappelli',
    # "semantic_admin",
    "validate_requests.apps.ValidateRequestsConfig",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #### Addons
    # 'bootstrap5',
    'django_admin_listfilter_dropdown',
    'rangefilter',
    #### Custom Application
    'formula_vcs.apps.FormulaVcsConfig',
    'members.apps.MembersConfig',
    'products.apps.ProductsConfig',
    'books.apps.BooksConfig',
    'upload_forecasts.apps.UploadForecastsConfig',
    'forecasts.apps.ForecastsConfig',
    'open_pds.apps.OpenPdsConfig',
    'confirm_invoices.apps.ConfirmInvoicesConfig',
    'receives.apps.ReceivesConfig',
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

ROOT_URLCONF = 'webbase.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'webbase.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # },
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        'NAME': os.environ.get('EDI_DBNAME'),
        'USER': os.environ.get('EDI_USERNAME'),
        'PASSWORD': os.environ.get('EDI_PASSWORD'),
        'HOST': os.environ.get('EDI_HOSTNAME'),
        'PORT': os.environ.get('EDI_PORT'),
    },
    'formula_vcst': {
        'ENGINE': 'mssql',
        'NAME': os.environ.get('FORMULA_DBNAME'),
        'USER': os.environ.get('FORMULA_USERNAME'),
        'PASSWORD': os.environ.get('FORMULA_PASSWORD'),
        'HOST': os.environ.get('FORMULA_HOSTNAME'),
        'PORT': os.environ.get('FORMULA_PORT'),
        "Trusted_Connection": "no",
        "OPTIONS": {"driver": "ODBC Driver 17 for SQL Server", },
    },
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

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Bangkok"
USE_I18N = True
USE_TZ = False

USE_THOUSAND_SEPARATOR = True
### Set Datetime Format
SHORT_DATE_FORMAT = "Y-m-d"
SHORT_DATETIME_FORMAT = "Y-m-d H:M:S"
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static",]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DATABASE_ROUTERS = ["webbase.db_routes.DBRoutes"]

APPEND_SLASH = False
AUTH_USER_MODEL = 'members.ManagementUser'
LOGIN_REDIRECT_URL = "forecast"

JAZZMIN_SETTINGS = {
    # # title of the window (Will default to current_admin_site.site_title if absent or None)
    # "site_title": "Web EDI Management",

    # # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    # "site_header": "EDI App",

    # # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "Web EDI Management",

    # # # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "image/menu_logo.png",

    # # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": "image/vcs_login.png",

    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,

    # CSS classes that are applied to the logo above
    # "site_logo_classes": "img-circle",

    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,

    # Welcome text on the login screen
    "welcome_sign": "Welcome to the Web EDI.",

    # Copyright on the footer
    "copyright": "Taweechai Yuenyang",

    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string
    # "search_model": ["auth.User", "auth.Group"],

    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,

    ############
    # Top Menu #
    ############

    # # Links to put along the top menu
    # "topmenu_links": [

    #     # Url that gets reversed (Permissions can be added)
    #     {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

    #     # external url that opens in a new window (Permissions can be added)
    #     {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

    #     # model admin to link to (Permissions checked against model)
    #     {"model": "auth.User"},

    #     # App with dropdown menu to all its models pages (Permissions checked against models)
    #     {"app": "books"},
    # ],

    #############
    # User Menu #
    #############

    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    # "usermenu_links": [
    #     {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
    #     {"model": "auth.user"}
    # ],

    #############
    # Side Menu #
    #############

    # Whether to display the side menu
    "show_sidebar": True,

    # Whether to aut expand the menu
    "navigation_expanded": True,

    # Hide these apps when generating side menu e.g (auth)
    # "hide_apps": ['upload_forecast'],

    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],

    # # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["upload_forecast", "forecasts", "open_pds","confirm_invoices", "receives","auth"],

    # Custom links to append to app groups, keyed on app name
    # "custom_links": {
    #     "books": [{
    #         "name": "Make Messages", 
    #         "url": "make_messages", 
    #         "icon": "fas fa-comments",
    #         "permissions": ["books.view_book"]
    #     }]
    # },

    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "users.Supplier": "fas fa-users",
        "products.ProductType": "fas fa-table",
        "products.Unit": "fas fa-tags",
        "books.RefType": "fas fa-layer-group",
        "books.EDIReviseType": "fas fa-thumbtack",
        "books.ReviseBook": "fas fa-bookmark",
        "products.Product": "fas fa-database",
        "products.ProductGroup": "fas fa-tags",
        "users.Position": "fas fa-key",
        "users.Section": "fas fa-id-card-alt",
        "users.Department": "fas fa-id-card",
        "books.Book": "fas fa-book",
        "users.ManagementUser": "fas fa-user-friends",
        "users.Factory": "fas fa-warehouse",
        "users.Corporation": "fas fa-building",
        "users.LineNotification": "fas fa-exclamation-circle",
        "users.Employee": "fas fa-database",
        'users.PlanningForecast': "fas fa-calendar",
        "users.OrganizationApprovePDS": "fas fa-sitemap",
        "forecasts.FileForecast": "fas fa-upload",
        'forecasts.Forecast': "fas fa-tasks",
        'open_pds.PDSHeader': "fas fa-file-invoice",
        # 'request_orders.PurchaseRequest': "fas fa-money-check",
        'receives.ReceiveHeader': "fas fa-file-invoice",
        'confirm_invoices.ConfirmInvoiceHeader': "fas fa-check-double",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",

    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": True,

    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": True,

    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {"auth.user": "collapsible", "auth.group": "vertical_tabs"},
    # Add a language dropdown into the admin
    # "language_chooser": True,
}
# JAZZMIN_UI_TWEAKS = {
#     "navbar_small_text": True,
#     "footer_small_text": True,
#     "body_small_text": True,
#     "brand_small_text": True,
#     "brand_colour": "navbar-cyan",
#     "accent": "accent-primary",
#     "navbar": "navbar-info navbar-dark",
#     "no_navbar_border": True,
#     "navbar_fixed": True,
#     "layout_boxed": False,
#     "footer_fixed": False,
#     "sidebar_fixed": True,
#     "sidebar": "sidebar-light-lightblue",
#     "sidebar_nav_small_text": True,
#     "sidebar_disable_expand": True,
#     "sidebar_nav_child_indent": True,
#     "sidebar_nav_compact_style": True,
#     "sidebar_nav_legacy_style": True,
#     "sidebar_nav_flat_style": True,
#     "theme": "united",
#     "dark_mode_theme": None,
#     "button_classes": {
#         "primary": "btn-primary",
#         "secondary": "btn-secondary",
#         "info": "btn-info",
#         "warning": "btn-warning",
#         "danger": "btn-danger",
#         "success": "btn-success"
#     },
#     "actions_sticky_top": False
# }

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": True,
    "brand_small_text": False,
    "brand_colour": "navbar-gray",
    "accent": "accent-lightblue",
    "navbar": "navbar-gray navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-teal",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": True,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "united",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True
}



JASPER_RESERVER = os.environ.get("JASPER_RESERVERVER")
JASPER_USER = os.environ.get("JASPER_USER")
JASPER_PASSWORD = os.environ.get("JASPER_PASSWORD")