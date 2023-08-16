from typing import Any, List, Dict
from fastapi import FastAPI, Depends, HTTPException, status
import redis
from redis import RedisError
import json
from dotenv import load_dotenv
import os
load_dotenv()

r = redis.Redis(
    host="redis-10522.c293.eu-central-1-1.ec2.cloud.redislabs.com",
    port=10522,
    password=os.getenv("redis_key"),
    decode_responses=True
)

# print all key, value pairs
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

# print all key, value pairs (startswith)
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

app = FastAPI(title="FastAPI CURD on Redis")

# Create route
@app.post("/create", tags=["CREATE"])
def create(key: str, value: Any):

    r.set(key, value)

    return {"message": "Record created successfully"}

# Create route for hash (dict)
@app.post("/create_dict", tags=["CREATE"])
def create_dict(key: str, value: dict):

    r.hset(key, mapping=value)

    return {"message": "Record created successfully"}

# Read route
@app.get("/read_one", tags=["READ"])
async def read(key: str):
    try:
        if not r.exists(key):
            raise RedisError("KEY_NOT_FOUND")
        
        type = r.type(key)
        if type == "string":
            val = r.get(key)
            return {"message": "Record read successfully", "value": val}
        elif type == "hash":
            vals = r.hgetall(key)
            return {"message": "Record read successfully", "value": vals}
        elif type == "zset":
            vals = r.zrange(key, 0, -1)
            return {"message": "Record read successfully", "value": vals}
        elif type == "list":
            vals = r.lrange(key, 0, -1)
            return {"message": "Record read successfully", "value": vals}
        elif type == "set":
            vals = r.smembers(key)
            return {"message": "Record read successfully", "value": vals}
    except RedisError as e:
        return {
            "message": f"Key not found: {e}",
            "error": True
        }, 500

# Get all key, value pairs
@app.get("/read_all", tags=["READ"])
def getall(allpairs: Dict = Depends(getallpairs)):
    return allpairs

# Get all that start with...
@app.get("/read_all_startwith", tags=["READ"])
def getall_startwith(allpairs_startwith: Dict = Depends(getallpairs_starswith)):
    return allpairs_startwith

# Update route
@app.put("/update", tags=["UPDATE"])
def update(key: str, value: Any):
    
    if not r.exists(key):
        return {"message": "Key not found"}
    
    r.set(key, value)
    
    return {"message": "Record updated successfully"}

# Update dict route
@app.put("/update_dict", tags=["UPDATE"])
def update(key: str, value: dict):
    
    if not r.exists(key):
        return {"message": "Key not found"}
    
    r.hset(key, mapping=value)
    
    return {"message": "Record updated successfully"}

# Delete route
@app.delete("/delete", tags=["DELETE"])
def delete(key: str):
    
    if not r.exists(key):
        return {"message": "Key not found"}
    
    r.delete(key)
    
    return {"message": "Record deleted successfully"}



# Delete keys that starts with certain text
@app.delete("/delete_startswith", tags=["DELETE"])
def delete_startswith(key: str):
    keys = r.keys(f"{key}*")
    if not keys:
        return {"message": f"No key found that starts with {key}"}
    
    for key in keys:
        r.delete(key)
        
    return {"message": "Records deleted successfully"}
