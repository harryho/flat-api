
from flask import Flask
# from flask import abort, request, make_response, current_app , Response

# from pprint import pprint as pp
from pseuserver import *
import json
# from json import dumps
# import sys
# import os

# from functools import wraps, partial
# import re
# import operator
# from collections import Mapping
# from urllib.parse import urlparse, urljoin

if __name__ == '__main__':

    app = Flask(__name__)
    restApi = PseuServer(app)
    app.run(debug=False)
