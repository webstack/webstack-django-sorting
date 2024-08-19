# Set up

1. Create a virtualenv (mkvirtualenv)
2. `pip install -r requirements.txt`
3. `pip install ..`
4. `./manage.py migrate` (the DB can be deleted by removing the file `db.sqlite3`)
5. `./manage.py loaddata secretfiles`
6. `./manage.py runserver`

To run tests: `./manage.py test`.
