# Set up

1. `rye sync`, **FIXME** Not able to use `rye add foo --path bar` to add my local dependency on `webstack-django-sorting`
2. `./manage.py migrate` (the DB can be deleted by removing the file `db.sqlite3`)
3. `./manage.py loaddata secretfiles`
4. `./manage.py runserver`

To run tests: `./manage.py test`.
