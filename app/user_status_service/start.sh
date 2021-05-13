#!/bin/bash

/usr/local/openresty/nginx/sbin/nginx -p / -c nginx/nginx.conf
python3 app/wsgi.py
