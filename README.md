## Local deployment using vagrant
* ``vagrant up``
* ``vagrant ssh``
* ``cd /vagrant``
* ``cp env.example ./config/.env``
*  ``./manage.py migrate``
* ``./manage.py runserver`` to run the server

## Celery worker start command

* ``celery -A arsmoon.taskapp worker -l info -n worker``

