rm blitz/usermedia/headshots/*.jp*
rm blitz/usermedia/headshots/*.png
rm blitz/usermedia/checkins/*.jp*
rm blitz/usermedia/checkins/*.png
rm blitz/usermedia/documents/*
rm blitz/usermedia/feed/*.jp*
rm blitz/usermedia/feed/*.png
rm blitz/usermedia/logos/*.jp*
rm blitz/usermedia/logos/*.png
mv blitz/usermedia/programs/sample_blitz_program.xls blitz/usermedia/programs/sample_blitz_program.KEEP
rm blitz/usermedia/programs/*.xls
mv blitz/usermedia/programs/sample_blitz_program.KEEP blitz/usermedia/programs/sample_blitz_program.xls

python manage.py syncdb --noinput
python manage.py migrate --all
python manage.py setup_test_env --traceback
python manage.py setup_new_stuff --traceback
python manage.py setup_headings --traceback
python manage.py setup_charge_env --traceback

