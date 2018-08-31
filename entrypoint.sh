#!/bin/bash

# make database migrations
python manage.py makemigrations --noinput --settings=cog.settings.development

# apply database migrations
python manage.py migrate --noinput --settings=cog.settings.development

# collect static files
python manage.py collectstatic --noinput --settings=cog.settings.development

# load admin
python manage.py loaddata admin.json --settings=cog.settings.development

exec "$@"