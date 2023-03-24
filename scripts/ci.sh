#!/bin/bash

cat > ./env/.env.prod << EOL
DJANGO_SETTINGS_MODULE = lotus.settings
PYTHONPATH = .
SECRET_KEY = ${SECRET_KEY}
STRIPE_LIVE_SECRET_KEY: ${SECRET_KEY}
STRIPE_TEST_SECRET_KEY: ${STRIPE_TEST_SECRET_KEY}
DEBUG = False
PYTHONDONTWRITEBYTECODE = 1
SELF_HOSTED = ${SELF_HOSTED}
DOCKERIZED = True
POSTGRES_USER = lotus
POSTGRES_PASSWORD = lotus
POSTGRES_DB = lotus
EOL