import unittest
from flask  import Flask, abort, request, make_response, current_app , Response
from pseuserver import *
from pseuserver.methods import *
import pseuserver
import requests
import json
from pprint import pprint as pp
import os
from pseudb import *



def test_server_api():
    endpoint = server_api('','', '' )

    pp(endpoint.__name__)
    pp(type(endpoint))
    assert endpoint is not None 
    assert callable(endpoint)
    assert endpoint.__name__ =='restapi'



if __name__ == "__main__":
    unittest.main()            