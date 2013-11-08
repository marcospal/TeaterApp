from settings import *
# Django local settings for teaterapp project.

LIVE = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'contabile2',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'contabile2',
        'PASSWORD': 'hest1234',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/home/tax/webapps/contabile2_static/' #/Users/jesper/TeaterApp/teaterapp/static/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    '/home/tax/webapps/contabile2/TeaterApp/teaterapp/static/',
    #'/Users/jesper/TeaterApp/teaterapp/static',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'mailbox_username'
EMAIL_HOST_PASSWORD = 'mailbox_password'
DEFAULT_FROM_EMAIL = 'valid_email_address'
SERVER_EMAIL = 'valid_email_address'