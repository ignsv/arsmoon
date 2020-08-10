## Local deployment using vagrant
* ``vagrant up``
* ``vagrant ssh``
* ``sudo add-apt-repository ppa:chris-lea/redis-server``
* ``sudo apt-get update``
* ``sudo apt -y install redis-server``
* ``cd /vagrant``
* ``cp env.example ./config/.env``
*  ``./manage.py migrate``
* ``./manage.py runserver`` to run the server


## websocket and swagger urls
* rest documentation ``/docs/``
* websocket ``ws://localhost:8000/ws/bitmex/``
