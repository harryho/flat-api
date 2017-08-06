Pseu-Server
----

|Build Status|

Pseu-Server is a **zero coding** restful API server inspired by Json-Server_ and Eve_. It is designed to be used as fake restful api for development, especially for people want to use Python stack. Setup process is **less than 1 minute*d*. 


Pseu-Sever is:

- **Flask based web server** Pseu-Server is built on the top of _Flask

- **Json flat file database** Pseu-Server uses PseuDB_ to manage the Json flat file database. PseuServer is a document oriented database. 

- **Zero coding to setup Restful API** Pseu-Sever is designed to use without coding. You just need one config to setup all endpoints you need, then you can use it immediately. 


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

        It is most easy way to test the API

    - Use curl 


.. code-block:: bash

    # Add a new post

    $ curl -d "{\"text\":\"post 1\",\"author\":\"harry\"}" -H "Content-Type: application/json" -X POST http://localhost:5000/posts
    {"author": "harry", "text": "post 1", "id": 1}

    # Get post by Id
    $ curl -X GET http://localhost:5000/posts/1
    {"author": "harry", "text": "post 1", "id": 1}
    
    # Get all posts
    $ curl -X GET http://localhost:5000/posts
    [{"author": "harry", "text": "post 1", "id": 1}]

    # Update  the post
    $ curl -d "{\"text\":\"post updated\",\"author\":\"harry\"}" -H "Content-Type: application/json" -X PUT http://localhost:5000/posts/1
    [{"author": "harry", "text": "post updated", "id": 1}]

    # Delete 
    $ curl -X DELETE http://localhost:5000/posts 


Stable release
**************

- Coming soon


Nightly build
*************

- |Pseu-Server 1.0.0 - RC1|

.. |Pseu-Server 1.0.0 - RC1| :target:: https://pypi.python.org/pypi?:action=display&name=pseuserver&version=1.0.0rc1

.. |Build Status| image:: https://travis-ci.org/harryho/pseu-server.svg?branch=master
    :target: https://travis-ci.org/harryho/pseu-server
.. _Flask: http://flask.pocoo.org/
.. _Eve: http://python-eve.org/
.. _Json-Server: https://github.com/typicode/json-server
.. _PseuServer: https://github.com/harryho/pseuserver
