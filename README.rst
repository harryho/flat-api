Pseu-Server
----

Pseu-Server is a *zero coding* restful API server inspired by Json-Server_ and Eve_. It is designed to be used as fake restful api for development, especially for people want to use Python stack. Setup process is *less than 1 minute*. 


Pseu-Sever is:

- **Flask based web server** Pseu-Server is built on the top of _Flask

- **Json flat file database** Pseu-Server uses PseuDB_ to manage the Json flat file database. PseuServer is a document oriented database. 

- **Zero coding to setup Restful API** Pseu-Sever is removed in PseuServer. User needs to create a table first before inserting any data. 


User guide
**********

- Create config.json

.. code-block:: json

    {
        "db": "db.json",
        "routes":[
            "/posts",
            "/comments"
        ]
    }

- Install Pseu-Server

.. code-block:: bash

    $ pip install pseuserver


- Launch Pseu-Server. Please make sure the config.json is under current diretory

.. code-block:: bash

    $ python3 pseuserver


- Test api

    - Use postman 

    - Use curl 



Stable release
**************

- Coming soon


Nightly build
*************

- Pseu-Server 1.0.0 - RC1

.. _Flask: http://flask.pocoo.org/
.. _Eve: http://python-eve.org/
.. _Json-Server: https://github.com/typicode/json-server
.. _PseuServer: https://github.com/harryho/pseuserver
