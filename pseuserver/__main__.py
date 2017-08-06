
from flask import Flask
from pseuserver import *
import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-P", "--port", type=int,
                    help="Customize the port")
    args = parser.parse_args()               
    _port = args.port or 5000
    app = Flask(__name__)
    restApi = PseuServer(app)
    app.run(debug=False, port = _port )
