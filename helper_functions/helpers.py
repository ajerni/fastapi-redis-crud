from connections.redis_db import REDIS_CLIENT as r
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