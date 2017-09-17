import sys

DEFAULT_CONFIG= 'config.json'
DEFAULT_DB = 'db.json'
DEFAULT_MEDIATYPE='application/json'
DEFAULT_API_PREFIX=''
FILE_STORAGE='FILE'
MEMORY_STORAGE='MEMORY'

PY3 = sys.version_info > (3,)

CONFIG_ROUTES = 'routes'
CONFIG_PREFIX = 'prefix'
CONFIG_DB = 'db'
CONFIG_STORAGE='storage'
CONFIG_CACHE='cache'

# RESOURCE_DB='db'
# RESOURCE_STORAGE='storage'
RESOURCE_QUERY='query'
RESOURCE_QUERY_LIKE='_like'
RESOURCE_QUERY_GREATER_THAN='_gt'
RESOURCE_QUERY_GREATER_THAN_AND_EQUAL='_gte'
RESOURCE_QUERY_LESS_THAN='_lt'
RESOURCE_QUERY_LESS_THAN_AND_EQUAL='_lte'
RESOURCE_DOCUMENT='doc'
RESOURCE_ID='id'
RESOURCE_EMBED='embed'
RESOURCE_EXPAND='expand'
RESOURCE_DATA='data'