#! /bin/sh

gunicorn --preload --workers=2 --timeout 60 -k eventlet -b :${API_PORT} did_communication_api.__main__:flask_app
