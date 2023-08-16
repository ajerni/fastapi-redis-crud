from typing import Any, Dict
from connections.redis_db import REDIS_CLIENT as r
from redis import RedisError

# get one key, value pair
def getone(key: str):

    def response(val: Any):
        return {"message": "Record read successfully", "value": val}

    try:
        if not r.exists(key):
            raise RedisError("KEY_NOT_FOUND")
        
        type = r.type(key)

        if type == "string":
            val = r.get(key)
            return response(val)
           
        elif type == "hash":
            val = r.hgetall(key)
            return response(val)
        elif type == "zset":
            val = r.zrange(key, 0, -1)
            return response(val)
        elif type == "list":
            val = r.lrange(key, 0, -1)
            return response(val)
        elif type == "set":
            val = r.smembers(key)
            return response(val)
        
    except RedisError as e:
        return {
            "message": f"Key not found: {e}",
        }

# get all key, value pairs
def getallpairs():
    pairs = []
    for key in r.keys("*"):
        type = r.type(key)
        if type == "string":
            val = r.get(key)
            pairs.append({"Key": key, "Value": val, "Type": type})
        if type == "hash":
            vals = r.hgetall(key)
            pairs.append({"Key": key, "Value": vals, "Type": type})
        if type == "zset":
            vals = r.zrange(key, 0, -1)
            pairs.append({"Key": key, "Value": vals, "Type": type})
        if type == "list":
            vals = r.lrange(key, 0, -1)
            pairs.append({"Key": key, "Value": vals, "Type": type})
        if type == "set":
            vals = r. smembers(key)
            pairs.append({"Key": key, "Value": vals, "Type": type})
    print(pairs)
    return {"messages": pairs}

# get all key, value pairs (startswith)
def getallpairs_starswith(key: str):
    keys = r.keys(f"{key}*")
    if not keys:
        return {"message": f"No key found that starts with {key}"}
    pairs = []
    for key in keys:
        type = r.type(key)
        if type == "string":
            val = r.get(key)
            pairs.append({"Key": key, "Value": val, "Type": type})
        if type == "hash":
            vals = r.hgetall(key)
            pairs.append({"Key": key, "Value": vals, "Type": type})
        if type == "zset":
            vals = r.zrange(key, 0, -1)
            pairs.append({"Key": key, "Value": vals, "Type": type})
        if type == "list":
            vals = r.lrange(key, 0, -1)
            pairs.append({"Key": key, "Value": vals, "Type": type})
        if type == "set":
            vals = r. smembers(key)
            pairs.append({"Key": key, "Value": vals, "Type": type})
    print(pairs)
    return {"messages": pairs}