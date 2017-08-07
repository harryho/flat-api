from flask import Flask, abort, request, make_response, current_app , Response
from pprint import pprint as pp
from json import dumps
from werkzeug.http import HTTP_STATUS_CODES
import re
from pseuserver.resource import *

import sys

try:
    from urlparse import parse_qsl
except ImportError:
    from urllib.parse import parse_qsl


from werkzeug.http import HTTP_STATUS_CODES

PY3 = sys.version_info > (3,)

""" Module that monkey-patches json module when it's imported so
JSONEncoder.default() automatically checks for a special "to_json()"
method and uses it to encode the object if found.
"""
from json import JSONEncoder

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder().default  # Save unmodified default.
JSONEncoder.default = _default # replacement


# def http_status_message(code):
#     """Maps an HTTP status code to the textual status"""
#     return HTTP_STATUS_CODES.get(code, '')


# def unpack(value):
#     """Return a three tuple of data, code, and headers"""
#     if not isinstance(value, tuple):
#         return value, 200, {}

#     try:
#         data, code, headers = value
#         return data, code, headers
#     except ValueError:
#         pass

#     try:
#         data, code = value
#         return data, code, {}
#     except ValueError:
#         pass

#     return value, 200, {}


def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""

    settings = current_app.config.get('RESTFUL_JSON', {})

    # If we're in debug mode, and the indent is not set, we set it to a
    # reasonable value here.  Note that this won't override any existing value
    # that was set.  We also set the "sort_keys" value.
    if current_app.debug:
        settings.setdefault('indent', 4)
        settings.setdefault('sort_keys', False)

    # always end the json dumps with a new line
    # see https://github.com/mitsuhiko/flask/pull/1262
    dumped = dumps(data, **settings) + "\n"
    
    resp = make_response(dumped, code)
    # resp.headers.extend(headers or {'Content-Type':'application/json'})
    resp.headers['Content-Type'] = 'application/json'
    return resp

def get(**kwargs):

    try:
        return output_json(query(**kwargs), 200)
    except Exception  as e:
        return output_json(e, 404)

def delete(**kwargs):
    try:
        return output_json(remove(**kwargs), 200)
    except Exception  as e:
        return output_json(e, 405)

def put(**kwargs):
    try:
        return output_json(edit(**kwargs), 200)
    except Exception  as e:
        return output_json(e, 405)       

def post(**kwargs):
    try:
        return output_json(create(**kwargs), 201)
    except Exception  as e:
        return output_json(e, 405)   

def server_api(prefix, urls, db):
    """Return function restapi as universal endpoint to process most
    common HTTP methods: GET, POST, PUT, DELETE. 
    :param prefix: The prefix of each endpoint
    :type prefix: string or bytes
    :param urls: The api routes for endpoints
    :type urls: array of string 
    :param db: The json database file path
    :type db: string or bytes
    """

    def restapi(**kwargs):
        _prefix = prefix
        _urls = urls
        _db = db

        response = None
        method = request.method

        req = request
        arg_dict = {}
        if len(kwargs):
            arg_dict[RESOURCE_QUERY] = kwargs

        qs = dict(parse_qsl(req.query_string.decode("utf-8")))
        # pp(qs)
        if RESOURCE_QUERY not in arg_dict:
            arg_dict[RESOURCE_QUERY]={}
        arg_dict[RESOURCE_QUERY].update(qs)
        arg_dict[RESOURCE_DB] = _db

        path = req.path

        for _url in _urls:
            if path.startswith(_prefix + _url):
                arg_dict[RESOURCE_DOCUMENT] = _url[_url.rfind('/')+1:]
                break

        if method in ('GET', 'HEAD'):
            response = get( **arg_dict)
        elif method == 'PUT':
            arg_dict[RESOURCE_DATA] = req.data
            print(arg_dict)
            response = put( **arg_dict)
        elif method == 'DELETE':
            response = delete( **arg_dict)
        elif method == 'POST':
            arg_dict[RESOURCE_DATA] = req.data
            response = post( **arg_dict)
        # elif method == 'OPTIONS':
        #     send_response(resource, response)
        else:
            abort(405)
        return response
   
    return restapi
