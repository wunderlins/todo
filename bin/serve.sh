#!/usr/bin/env bash

app=www
bin=uwsgi
port=7400

$bin  --plugin python,http \
      --http :$port \
      --check-static www/ \
      --static-index index.html \
      --pidfile var/$app.pid \
      --logto var/$app.log \
      --workers 1 \
      --single-interpreter
#      --static-index index.htm --static-index default.html \
#      --plugin python,http \
#      --static-map /=www/ \
#      --wsgi-file httpd.py \
#      --plugins-dir "$basedir/lib" \
#      --daemonize $web_logfile \
#      --daemonize2 var/uwsgi.log
