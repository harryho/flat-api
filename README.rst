FlatApi
----

|Build Status| |Coverage| |Version|

FlatApi is a **zero coding** and **zero configuration** restful API server inspired by Json-Server_ and Eve_. It is designed to be used as fake restful api for development, especially for people want to use Python stack. Setup process is **less than 10 seconds**. 


FlatApi is:

- **Zero coding and configuration to setup Restful API** FlatApi is designed to use without coding and configuration by default. You just need one config to setup all endpoints you need, then you can use it immediately. 

- **Flask based web server** FlatApi is built on the top of _Flask

- **Json flat file database** FlatApi uses FlatApi_ to manage the Json flat file database. FlatApi is a document oriented database. 

- **Caching memory storage availble** FlatApi supports caching momery storage after version 4.0.0. 

Install Package
***************

.. code-block:: bash

    $ pip uninstall flatapi
    $ pip install --no-cache-dir flatapi


Quick Start
***********

- Launch FlatApi without configuration

.. code-block:: bash
    # Start the FlatApi - Sample 1 
    python3 /<path_to_package>/flatapi -S MEMORY -G NO
    # Start the FlatApi - Sample 2
    python3 /<path_to_package>/flatapi --storage MEMORY -cfgfile NO

.. code-block:: bash

    \(^_^)/ Hi

    Loading  is done.

    There is no config file found. Flat Api uses internal configuration.

    Resource :
    /<string:doc> -- The doc is the collection name
                        you want to post or put the object.
    /<string:doc>/<int:id> --The id is the unique id for query or delete.

    Database: Memory

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


Custom Configuration
********************

- Create config.json as sample below (There is a sample in the repo as well)

.. code-block:: json

    {
        "db": "db.json",
        "routes":[
            "/posts",
            "/comments"
        ]
    }

- Launch FlatApi. Please make sure the config.json is under current diretory

.. code-block:: bash
    
    $ python3 /<path_to_package>/flatapi 

     \(^_^)/ Hi

    Loading config.json is done.

    Resource :
    /posts
    /comments

    Database: db.json

    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)




Advanced usage
**************

- **Change default port**

.. code-block:: bash

    $ python3 flatapi -P 4999
    ...
    * Running on http://127.0.0.1:4999/ (Press CTRL+C to quit)

- **Add prefix to the API via config.json**

.. code-block:: json

    {
        "db":"db.json",
        "prefix": "api",
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
            "id": 1,
            "recommended": 4
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
        "id": 1,
        "recommended": 4
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
        "id": 1,
        "recommended": 4
    }

- Use query string to retrieve the objects

.. code-block:: bash

    GET /posts?author=harry


- Following is query result 


.. code-block:: json

    {
        "author": "harry",
        "text": "post 1",
        "id": 1,
        "recommended": 4
    }

- Use `_like` to retrieve the objects

.. code-block:: bash

    GET /posts?text_like=4


- Following is query result 


.. code-block:: json

    {
        "author": "harry",
        "text": "post 1",
        "id": 1,
        "recommended": 4
    }

- Use `_gte`, `_gt`, `_lt`, `_lte` to retrieve the objects

.. code-block:: bash

    GET /posts?recommended_gte=4


- Following is query result 

.. code-block:: json

    {
        "author": "harry",
        "text": "post 1",
        "id": 1,
        "recommended": 4
    }

- **Use caching momery storage**

- Use following config to launch the api with caching memory storage.  

.. code-block:: json

    {
        "storage": "MEMORY",
        "routes":[
            "/posts",
            "/comments"
        ]
    }   




.. |Build Status| image:: https://travis-ci.org/harryho/flat-api.svg?branch=master
    :target: https://travis-ci.org/harryho/flat-api
.. |Coverage| image:: https://coveralls.io/repos/github/harryho/flat-api/badge.svg?branch=master
    :target: https://coveralls.io/github/harryho/flat-api?branch=master

.. |Version| image:: https://badge.fury.io/py/flatapi.svg
    :target: https://badge.fury.io/py/flatapi

.. _Flask: http://flask.pocoo.org/
.. _Eve: http://python-eve.org/
.. _Json-Server: https://github.com/typicode/json-server
.. _FlatApi: https://github.com/harryho/flata
