Pseu-Server
----

|Build Status| |Coverage| |Version|

Pseu-Server is a **zero coding** restful API server inspired by Json-Server_ and Eve_. It is designed to be used as fake restful api for development, especially for people want to use Python stack. Setup process is **less than 1 minute*d*. 


Pseu-Sever is:

- **Flask based web server** Pseu-Server is built on the top of _Flask

- **Json flat file database** Pseu-Server uses PseuDB_ to manage the Json flat file database. PseuServer is a document oriented database. 

- **Zero coding to setup Restful API** Pseu-Sever is designed to use without coding. You just need one config to setup all endpoints you need, then you can use it immediately. 


Quick Start
***********

- Create config.json as sample below (There is a sample in the repo as well)

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
     \(^_^)/ Hi

    Loading config.json is done.

    Resource :
    /posts
    /comments

    Database: db.json

    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

- Test api via postman 

    It would be a much more handy and easy way to play around with the API immediately.

.. code-block:: bash

    GET /posts       --> Get all posts
    POST /posts      --> Add new post
    PUT /posts/1     --> Update existing post which id is 1
    DELETE /posts/1  --> Delete a post which id is 1
    DELETE /posts    --> Delete all posts

- Test api via curl 

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


Advanced usage
**************

- **Change default port**

.. code-block:: bash

    $ python3 pseuserver -P 4999
    ...
    * Running on http://127.0.0.1:4999/ (Press CTRL+C to quit)

- **Add prefix to the API via config.json**

.. code-block:: json

    {
        "db":"db.json",
        "prefix": "/api"
        "routes":[
            "/posts",
            "/comments"
        ]
    }

- API changes as follows

.. code-block:: bash

    GET /api/posts       --> Get all posts
    GET /api/posts/1     --> Get the post which id is 1
    POST /api/posts      --> Add new post
    PUT /api/posts/1     --> Update existing post which id is 1
    DELETE /api/posts/1  --> Delete a post which id is 1
    DELETE /api/posts    --> Delete all posts

- **Advanced queries**


- Create sample test data in db.json

.. code-block:: json

    {
        "posts": [{
            "author": "harry",
            "text": "post 1",
            "id": 1
        }],
        "comments": [{
            "postId": 1,
            "commentator": "john",
            "text": "comment  1",
            "id": 1
        }]
    }

- Use built-in embed route setting to retrieve children objects. It is inspired by Json-Server.

.. code-block:: bash

    GET /posts/1/comments


- Following is query result

.. code-block:: json

    {
        "author": "harry",
        "comments": [
            {
                "postId": 1,
                "commentator": "john",
                "text": "comment  1",
                "id": 1
            }
        ],
        "text": "post 1",
        "id": 1
    }


-  Use expand to retrieve parent objects

.. code-block:: bash

    GET /comments/1?expand=posts


- Following is query result


.. code-block:: json
          
    {
        "postId": 1,
        "commentator": "john",
        "post": {
            "author": "harry",
            "text": "post 1",
            "id": 1
        },
        "text": "comment  1",
        "id": 1
    }

- Use query string to retrieve the objects

.. code-block:: bash

    GET /posts?author=harry


- Following is query result 


.. code-block:: json

    {
        "author": "harry",
        "text": "post 1",
        "id": 1
    }

Stable release
**************

- |Pseu-Server 3.0.0|

.. |Pseu-Server 3.0.0| :target:: https://pypi.python.org/pypi?:action=display&name=pseuserver&version=2.5.0

.. |Build Status| image:: https://travis-ci.org/harryho/pseu-server.svg?branch=master
    :target: https://travis-ci.org/harryho/pseu-server
.. |Coverage| image:: https://coveralls.io/repos/github/harryho/pseu-server/badge.svg?branch=master
    :target: https://coveralls.io/github/harryho/pseu-server?branch=master
.. |Version| image:: http://img.shields.io/pypi/v/pseuserver.svg?style=flat-square
    :target: https://pypi.python.org/pypi/pseuserver/

.. _Flask: http://flask.pocoo.org/
.. _Eve: http://python-eve.org/
.. _Json-Server: https://github.com/typicode/json-server
.. _PseuServer: https://github.com/harryho/pseu-server
