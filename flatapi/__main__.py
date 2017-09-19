
from flask import Flask
from flatapi import *
import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-P", "--port", type=int,
                    help="Customize the port")
    parser.add_argument("-G", "--cfgfile", 
                    help="Customize the config file option: DEFAULT | NO | <file_name>") 
    parser.add_argument("-S", "--storage", 
                    help="Customize the storage. Option: FILE | MEMORY ")  
    parser.add_argument("-X", "--prefix", 
                    help="Customize the prefix, e.g. api")

    args = parser.parse_args()               
    _port = args.port or 5000

    _cfgfile = args.cfgfile 
    if _cfgfile:
        if _cfgfile.upper() == 'DEFAULT':
            _cfgfile = DEFAULT_CONFIG
        elif _cfgfile.upper() == 'NO':
            _cfgfile = None
    else:
        _cfgfile = DEFAULT_CONFIG

    _prefix = args.prefix
    _storage = args.storage.upper() if args.storage else args.storage

    
    # print ('\n     prefix:   %s' %(_prefix))
    # print ('    storage:   %s' %(_storage))

    app = Flask(__name__)
    restApi = FlatApi(app, cfg_file=_cfgfile, prefix = _prefix , storage = _storage)
    app.run(debug=False, port = _port )
