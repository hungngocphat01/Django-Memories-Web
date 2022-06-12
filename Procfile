release: cd source && python manage.py migrate
web: gunicorn --chdir source memories.wsgi --log-file -