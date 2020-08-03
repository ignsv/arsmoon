## Local deployment using vagrant
* ``sudo add-apt-repository ppa:chris-lea/redis-server``
* ``sudo apt-get update``
* ``sudo apt -y install redis-server``
* ``vagrant up``
* ``vagrant ssh``
* ``cd /vagrant``
* ``cp env.example ./config/.env``
*  ``./manage.py migrate``
* ``./manage.py runserver`` to run the server

## Celery worker start command

* ``celery -A arsmoon.taskapp worker -l info -n worker``


## websocket and swagger urls
* rest documentation ``/docs/``
* websocket ``ws://localhost:8000/ws/bitmex/``
