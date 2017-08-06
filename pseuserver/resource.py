from pseudb import PseuDB, where, Query
from pseudb.storages import JSONStorage
from pseuserver.settings import *
from json import loads, dumps
from pprint import pprint as pp

def extract_query(**kwqry):
    _query = None

    print('extract_query')
    for key in kwqry:
        if key != RESOURCE_ID and key != RESOURCE_EMBED and key != RESOURCE_EXPAND:
            value = kwqry[key]
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

    print( _id)
    print(_query)
    with PseuDB( _dbf, storage=JSONStorage) as db:
        tb =  db.table(_tb)
        if _id:
            print( _id)
            obj = tb.get(oid = _id)
            print( type(obj))

            if _embed and obj: 
                print(_embed)
                embed = db.table(_embed)
                print(embed)
                embed_id = _tb[:-1] + 'Id'
                embeds = embed.search(where(embed_id) == _id)
                pp( embeds)
                obj[_embed] = embeds
            
            if _expand and obj: 
                print(_expand)
                expand_id_field = expand_field = _expand[:-1] + 'Id'

                if expand_id_field in obj:
                    expand_id = obj[expand_id_field]
                    expand = db.table(_expand)
                    expand_field = _expand[:-1] 
                    expand_elem = expand.get(oid = _id)
                    pp( expand_elem)
                    obj[expand_field] = expand_elem
            pp(obj)

        elif _query:
            print(_query)
            obj = tb.search(_query)
            print(obj)
        else:
            obj = tb.all()
        return obj



def create(**kwargs):
    _dbf = kwargs[CONFIG_DB] or DEFAULT_DB
    _tb = kwargs[RESOURCE_DOCUMENT]
    _data = kwargs[RESOURCE_DATA]
    with PseuDB( _dbf, storage=JSONStorage) as db:
        tb =  db.table(_tb)
        obj = tb.insert(loads(_data.decode()))
        return obj

def remove(**kwargs):
    _dbf = kwargs[CONFIG_DB] or DEFAULT_DB
    _tb = kwargs[RESOURCE_DOCUMENT]
    _id = kwargs[RESOURCE_QUERY][RESOURCE_ID] \
        if RESOURCE_QUERY in kwargs and \
             RESOURCE_ID in kwargs[RESOURCE_QUERY] else None

    with PseuDB( _dbf, storage=JSONStorage) as db:
        tb =  db.table(_tb)
        if _id:
            rst = tb.remove(oids = [_id])
        else:
            rst = tb.purge()            
        return rst

def edit(**kwargs):
    _dbf = kwargs[CONFIG_DB] or DEFAULT_DB
    _tb = kwargs[RESOURCE_DOCUMENT]
    _data = kwargs[RESOURCE_DATA]
    _id = kwargs[RESOURCE_QUERY][RESOURCE_ID]
    
    with PseuDB( _dbf, storage=JSONStorage) as db:
        tb =  db.table(_tb)
        ids, objs = tb.update(loads(_data.decode()), oids = [_id])
        # print(ids, objs)
        return objs