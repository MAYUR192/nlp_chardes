#!/usr/bin/env sh
set -eu
cp /etc/nginx/sites-enabled/flask.conf /etc/nginx/sites-enabled/flask_test.conf
envsubst '${PORT}' < /etc/nginx/sites-enabled/flask_test.conf>  /etc/nginx/sites-enabled/flask.conf
if [ -f /etc/nginx/sites-enabled/flask_test.conf ]
then
	rm -f /etc/nginx/sites-enabled/flask_test.conf
fi
exec "$@"