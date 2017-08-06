import sys

__version__ = '0.1'

DEFAULT_CONFIG= 'config.json'
DEFAULT_DB = 'db.json'
DEFAULT_MEDIATYPE='application/json'
DEFAULT_API_PREFIX=''


PY3 = sys.version_info > (3,)

CONFIG_ROUTES = 'routes'
CONFIG_PREFIX = 'prefix'
CONFIG_DB = 'db'

RESOURCE_DB='db'
RESOURCE_QUERY='query'
RESOURCE_DOCUMENT='doc'
RESOURCE_ID='id'
RESOURCE_EMBED='embed'
RESOURCE_EXPAND='expand'
RESOURCE_DATA='data'