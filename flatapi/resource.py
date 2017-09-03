from flata import Flata, where, Query
from flata.storages import JSONStorage
from flatapi.settings import *
from json import loads, dumps
from pprint import pprint as pp

def extract_query(**kwqry):
    _query = None

    for key in kwqry:
        if key != RESOURCE_ID and key != RESOURCE_EMBED and key != RESOURCE_EXPAND:
            value = kwqry[key]

            if key.endswith(RESOURCE_QUERY_LIKE):                
                key = key[0:len(RESOURCE_QUERY_LIKE)*-1]
                _query = (_query) & (where(key).search(value)) if _query is not None else where(key).search(value)
            
            elif key.endswith(RESOURCE_QUERY_GREATER_THAN):                
                key = key[0:len(RESOURCE_QUERY_GREATER_THAN)*-1]
                _query = (_query) & (where(key) > value ) if _query is not None else where(key) > value
            
            elif key.endswith(RESOURCE_QUERY_LESS_THAN):                
                key = key[0:len(RESOURCE_QUERY_LESS_THAN)*-1]
                _query = (_query) & (where(key) < value ) if _query is not None else where(key) < value
            
            elif key.endswith(RESOURCE_QUERY_GREATER_THAN_AND_EQUAL):                
                key = key[0:len(RESOURCE_QUERY_GREATER_THAN_AND_EQUAL)*-1]
                _query = (_query) & (where(key) >= value ) if _query is not None else where(key) >= value
            
            elif key.endswith(RESOURCE_QUERY_LESS_THAN_AND_EQUAL):                
                key = key[0:len(RESOURCE_QUERY_LESS_THAN_AND_EQUAL)*-1]
                _query = (_query) & (where(key) <= value ) if _query is not None else where(key) <= value

            else: 
                _query = (_query) & (where(key) == value) if _query is not None else where(key) == value    
    
    return _query

    

def query(**kwargs):
    _dbf = kwargs[CONFIG_DB] or DEFAULT_DB
    _tb = kwargs[RESOURCE_DOCUMENT]

    _id = kwargs[RESOURCE_QUERY].pop(RESOURCE_ID) \
        if RESOURCE_QUERY in kwargs and RESOURCE_ID in kwargs[RESOURCE_QUERY] else None

    _embed = kwargs[RESOURCE_QUERY].pop(RESOURCE_EMBED) \
        if RESOURCE_QUERY in kwargs and RESOURCE_EMBED in kwargs[RESOURCE_QUERY] else None

    _expand = kwargs[RESOURCE_QUERY].pop(RESOURCE_EXPAND) \
        if RESOURCE_QUERY in kwargs and RESOURCE_EXPAND in kwargs[RESOURCE_QUERY] else None

    _query = extract_query(**kwargs[RESOURCE_QUERY]) if RESOURCE_QUERY in kwargs else None

    with Flata( _dbf, storage=JSONStorage) as db:
        tb =  db.table(_tb)
        if _id:
            obj = tb.get(id = _id)

            if _embed and obj: 
                embed = db.table(_embed)
                embed_id = _tb[:-1] + 'Id'
                embeds = embed.search(where(embed_id) == _id)
                obj[_embed] = embeds
            
            if _expand and obj: 
                expand_id_field = expand_field = _expand[:-1] + 'Id'

                if expand_id_field in obj:
                    expand_id = obj[expand_id_field]
                    expand = db.table(_expand)
                    expand_field = _expand[:-1] 
                    expand_elem = expand.get(id = _id)

                    obj[expand_field] = expand_elem

        elif _query:
            obj = tb.search(_query)

        else:
            obj = tb.all()
        return obj

def create(**kwargs):
    _dbf = kwargs[CONFIG_DB] or DEFAULT_DB
    _tb = kwargs[RESOURCE_DOCUMENT]
    _data = kwargs[RESOURCE_DATA]
    with Flata( _dbf, storage=JSONStorage) as db:
        tb =  db.table(_tb)
        obj = tb.insert(loads(_data.decode()))
        return obj

def remove(**kwargs):
    _dbf = kwargs[CONFIG_DB] or DEFAULT_DB
    _tb = kwargs[RESOURCE_DOCUMENT]
    _id = kwargs[RESOURCE_QUERY][RESOURCE_ID] \
        if RESOURCE_QUERY in kwargs and \
             RESOURCE_ID in kwargs[RESOURCE_QUERY] else None

    with Flata( _dbf, storage=JSONStorage) as db:
        tb =  db.table(_tb)
        if _id:
            rst = tb.remove(ids = [_id])
        else:
            rst = tb.purge()            
        return rst

def edit(**kwargs):
    _dbf = kwargs[CONFIG_DB] or DEFAULT_DB
    _tb = kwargs[RESOURCE_DOCUMENT]
    _data = kwargs[RESOURCE_DATA]
    _id = kwargs[RESOURCE_QUERY][RESOURCE_ID]
    
    with Flata( _dbf, storage=JSONStorage) as db:
        tb =  db.table(_tb)
        ids, objs = tb.update(loads(_data.decode()), ids = [_id])
        return objs