web: daphne deliveet.asgi:application -p $PORT -b 0.0.0.0 -v2 --access-logfile-
worker: python manage.py runworker -v2
release: ./manage.py migrate --no-input
