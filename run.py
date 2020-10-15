import sys
sys.dont_write_bytecode = True

app_label = 'introspective_admin'

import os
from django.conf import settings
from django.contrib import admin
from credentials import credentials


PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(PROJECT_PATH))

settings.configure(
    DEBUG=True,
    SECRET_KEY='thisisthesecretkey',
    ROOT_URLCONF=__name__,
    MIDDLEWARE_CLASSES=(
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ),
    DATABASES={
        'default': {
            'ENGINE': credentials['engine'],
            'NAME': credentials['database'],
            'USER': credentials['user'],
            'PASSWORD': credentials['password'],
            'HOST': credentials['host'],
            'PORT': credentials['port'],
        }
    },
    INSTALLED_APPS=[
        'introspective_admin',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ],
    MIDDLEWARE = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ),
    STATIC_ROOT = os.path.join(PROJECT_PATH, 'static'),
    STATIC_URL = '/static/',
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                # PROJECT_PATH + '/templates',
                # insert your TEMPLATE_DIRS here
            ],
            'OPTIONS': {
                'debug': True,
                'loaders': [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    'admin_tools.template_loaders.Loader',
                ],
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.request',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ],
)

import django
django.setup()
from django.core.management import execute_from_command_line
from django.conf.urls import url
from django.urls import path, re_path
from django.http import HttpResponse

from django.db import DEFAULT_DB_ALIAS, connections
# from django.core.management.commands.inspectdb import Command as InspectDB
from inspectdb import Command as InspectDB
from django.db import models




models_code = ""
for line in InspectDB().handle_inspection({
    'database': DEFAULT_DB_ALIAS,
    'include_partitions': False,
    'include_views': False,
    'table': '',
    'table_name_filter': lambda name: not name.startswith("auth_") and not name.startswith("django_"),
    'app_label': app_label,
}):
    if line != "from django.db import models":
        models_code += line + "\n"

# print(models_code)
eval(compile(models_code, '<string>', 'exec'))


# admin.site.register(Users)
from django.contrib import admin
from django.apps import apps
from django.contrib.admin import AdminSite
from django.contrib.admin.sites import AlreadyRegistered



app_models = apps.get_app_config('introspective_admin').get_models()
for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass


urlpatterns = [
    path('', admin.site.urls),
]

if __name__ == "__main__":
    if len(sys.argv) > 1:
        execute_from_command_line(sys.argv)
    else:
        execute_from_command_line(['', 'runserver'])
