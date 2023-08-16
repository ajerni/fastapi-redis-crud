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

blogs = {
    "name": "blogs",
    "1": "1. FastApi Prerequistiee",
    "2": "2. Building APIs with FastAPI",
    "3": "3. Background Tasks - Celery x FastAPI",
}

users = {"name": "users", "8": "Jamie", "9": "Roman"}

r.set("blog_key", json.dumps(blogs))
r.set("users_key", json.dumps(users))
r.set("gugus", "guguseli jattutuuuu")

#print(r.get("users_key"))

r.hset('userset:1', mapping={
    'name': 'John',
    "surname": 'Smith',
    "company": 'Redis',
    "age": 29
})

r.hset('blogset:1', mapping=blogs)

#print(r.hgetall('userset:1'))

# delete keys
def delete_startswith(key: str):
    for key in r.keys("blog*"):
        # delete the key
        r.delete(key)
    

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

class GetObjectOr404:
    def __init__(self, model) -> None:
        self.model = model
    def __call__(self, id: str):
        obj = self.model.get(id)
        if not obj:
            raise HTTPException(
                detail=f"Object with id {id} does not exist",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return obj

blog_dependency = GetObjectOr404(blogs)
@app.get("/blog/{id}", tags=["Blog"])
def get_blog(blog_name: str = Depends(blog_dependency)):
    return blog_name

user_dependency = GetObjectOr404(users)
@app.get("/user/{id}", tags=["Blog"])
def get_user(user_name: str = Depends(user_dependency)):
    return user_name

# Create route
@app.post("/create", tags=["CREATE"])
def create(key: str, value: Any):

    r.set(key, value)

    return {"message": "Record created successfully"}

# Read route
@app.get("/read", tags=["READ"])
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

# Update route
@app.put("/update", tags=["UPDATE"])
def update(key: str, value: Any):
    
    if not r.exists(key):
        return {"message": "Key not found"}
    
    r.set(key, value)
    
    return {"message": "Record updated successfully"}

# Delete route
@app.delete("/delete", tags=["DELETE"])
def delete(key: str):
    
    if not r.exists(key):
        return {"message": "Key not found"}
    
    r.delete(key)
    
    return {"message": "Record deleted successfully"}

# Get all key, value pairs
@app.get("/getall", tags=["READ"])
def getall(allpairs: Dict = Depends(getallpairs)):
    return allpairs

# Delete keys that starts with certain text
@app.delete("/delete_startswith", tags=["DELETE"])
def delete_startswith(key: str):
    keys = r.keys(f"{key}*")
    if not keys:
        return {"message": f"No key found that starts with {key}"}
    
    for key in keys:
        r.delete(key)
        
    return {"message": "Records deleted successfully"}

# Get all that start with...
@app.get("/getall_startwith", tags=["READ"])
def getall_startwith(allpairs_startwith: Dict = Depends(getallpairs_starswith)):
    return allpairs_startwith