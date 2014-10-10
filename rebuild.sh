python manage.py syncdb --noinput
python manage.py migrate --all
python manage.py setup_test_env --traceback
python manage.py setup_new_stuff --traceback

