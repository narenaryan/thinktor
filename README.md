# thinktor
A tornado and RethinkDB real-time Data Push engine

This project uses Python Tornado web browser and RethinkDB to notify superheroes real time.

just install requirements

~~~
$ pip install requirements.txt
$ python app.py
~~~

Visit http://localhost:8000 to see the website.

Note: First install rethinkDB server using below commands
~~~

$ source /etc/lsb-release && echo "deb http://download.rethinkdb.com/apt $DISTRIB_CODENAME main" | sudo tee /etc/apt/sources.list.d/rethinkdb.list
$ wget -qO- http://download.rethinkdb.com/apt/pubkey.gpg | sudo apt-key add -
$ sudo apt-get update
$ sudo apt-get install rethinkdb
$ sudo cp /etc/rethinkdb/default.conf.sample /etc/rethinkdb/instances.d/instance1.conf
$ sudo /etc/init.d/rethinkdb restart

~~~
