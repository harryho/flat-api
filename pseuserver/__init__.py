"""
PseuServer is a zero-coding, restful fake api web server for developers.

PseuServer provides most common GET, POST, PUT, DELETE methods with a configurable
backend. It has support for handy querying as well.

.. codeauthor:: Harry Ho <harry.ho_long@yahoo.com>

Usage example:

- Create a file *config.json* as following sample

{
    "db": "db.json",
    "prefix" : "",
    "routes":[
        "/posts",
        "/comments"
    ]
}

- Launch the server
>>> python pseuserver

- Test the restful API

$ curl  

"""

from flask import Flask
from flask import abort, request, make_response, current_app , Response

from pprint import pprint as pp
from pseuserver.methods import *
import json
# from json import dumps
import sys
import os

from functools import wraps, partial
import re
import operator
from collections import Mapping
# from urllib.parse import urlparse, urljoin

from pseuserver.settings import *



class PseuServer(object):

    def __init__(self, app=None, prefix='' , cfg_file = ''):

        self.this_directory = os.path.dirname(os.path.realpath(__file__))

        self.urls = {}
        self.routes = []
        self.prefix = prefix or DEFAULT_API_PREFIX
        self.default_mediatype = DEFAULT_MEDIATYPE
        self.app = None
        self.config_file = cfg_file or DEFAULT_CONFIG
        # self.config_file = os.path.join(os.getcwd(), cfg_file) \
        #     if cfg_file else os.path.join(os.getcwd(), DEFAULT_CONFIG)
        self.db_file = None
        self.db = DEFAULT_DB

        if app is not None:
            self.app = app
            self.load_routes()
            self.add_routes()

    def _complete_routes(self, url_part):
        """This method is used to defer the construction of the final url
        :param url_part: The part of the url the endpoint is registered with
        """
        basic_routes = ['', '/', '/<int:id>', '/<int:id>/<string:embed>']

        for i in range(len(basic_routes)):
            basic_routes[i] = '%s%s%s' % ( self.prefix , url_part , basic_routes[i])

        return basic_routes 


    def load_routes(self):

        # self.this_directory = os.path.dirname(os.path.realpath(__file__))
               

        if os.path.exists(self.config_file):
            self.this_directory = os.path.dirname(self.config_file)
        else:
            self.config_file = os.path.join(os.getcwd(), self.config_file) 

            if os.path.exists(self.config_file):
                self.this_directory = os.path.dirname(self.config_file)
            else:                
                raise ValueError('The %s is not found.' % DEFAULT_CONFIG)       
            
        
        with open(self.config_file) as cfg:
            data = json.load(cfg)
            if data:
                try:
                    self.urls = data[CONFIG_ROUTES]
                    self.prefix = data[CONFIG_PREFIX] if CONFIG_PREFIX in data else self.prefix
                    self.db = data[CONFIG_DB] if CONFIG_DB in data else DEFAULT_DB
                    self.db_file = os.path.join(self.this_directory, self.db)
                except ValueError as e:
                    raise ValueError('The routes is missing in the %s file. '% self.config_file )
            else:
                raise ValueError('The config.json file should not be empty.')
        
    
    def add_routes(self, **kwargs):
        rest_api = server_api(self.prefix, self.urls, self.db_file)
        for url in self.urls:
            rules = self._complete_routes(url)
            # pp(rules)
            for r in range(len(rules)):
                rule = rules[r]
                self.routes.append(rule)
                if r == 0: # e.g. /api/posts -> GET, POST
                    self.app.add_url_rule(rule, view_func=rest_api, methods=['GET', 'POST', 'DELETE'])
                if r == 1:  # e.g. /api/posts/ -> GET, POST
                    self.app.add_url_rule(rule, view_func=rest_api, methods=['GET', 'POST', 'DELETE'])
                elif r == 2: # e.g. /api/posts/1 -> GET, PUT, DELTETE
                    self.app.add_url_rule(rule, view_func=rest_api, methods=['GET', 'PUT', 'DELETE'])
                elif r == 3: # e.g. /api/posts/1/comments -> GET
                    self.app.add_url_rule(rule, view_func=rest_api, methods=['GET'])

# if __name__ == '__main__':
#     app = Flask(__name__)
#     restApi = PseuServer(app)
#     app.run(debug=False)



# __all__= ['PseuServer']
# __all__ = ('PseuServer')