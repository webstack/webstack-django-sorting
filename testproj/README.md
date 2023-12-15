# Set up

1. Create a virtualenv (mkvirtualenv)
2. `pip install -r requirements.txt`
3. `pip install ..`
4. `./manage.py migrate` (the DB can be deleted by removing the file `db.sqlite3`)
5. `./manage.py loaddata secretfiles`
6. `./manage.py runserver`

Available URLs:

- <http://127.0.0.1:8000/>
- <http://127.0.0.1:8000/nulls/first>
- <http://127.0.0.1:8000/nulls/last>
- <http://127.0.0.1:8000/jinja>
- <http://127.0.0.1:8000/jinja/nulls/first>
- <http://127.0.0.1:8000/jinja/nulls/last>

To run tests: `./manage.py test`.
