from typing import Any, Dict
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from connections.redis_db import REDIS_CLIENT as r
from redis import RedisError
from frontend.index_html import html
from helper_functions.helpers import getallpairs, getallpairs_starswith

app = FastAPI(title="FastAPI CURD on Redis")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

#root route - see frontend
@app.get("/", tags=["Frontend Landing Page"])
async def root():
    return HTMLResponse(html)

### CRUD ###

## Create ##

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

## READ ##

# Read route
@app.get("/read_one", tags=["READ"])
async def read_one(key: str):
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

# Read all key, value pairs
@app.get("/read_all", tags=["READ"])
def read_all(allpairs: Dict = Depends(getallpairs)):
    return allpairs

# Read all key, value pais that start with
@app.get("/read_all_startwith", tags=["READ"])
def read_all_startwith(allpairs_startwith: Dict = Depends(getallpairs_starswith)):
    return allpairs_startwith

## UPDATE ##

# Update route
@app.put("/update", tags=["UPDATE"])
def update(key: str, value: Any):
    
    if not r.exists(key):
        return {"message": "Key not found"}
    
    r.set(key, value)
    
    return {"message": "Record updated successfully"}

# Update dict route
@app.put("/update_dict", tags=["UPDATE"])
def update_dict(key: str, value: dict):
    
    if not r.exists(key):
        return {"message": "Key not found"}
    
    r.hset(key, mapping=value)
    
    return {"message": "Record updated successfully"}

## DELETE ##

# Delete route
@app.delete("/delete", tags=["DELETE"])
def delete(key: str):
    
    if not r.exists(key):
        return {"message": "Key not found"}
    
    r.delete(key)
    
    return {"message": "Record deleted successfully"}

# Delete keys that starts with
@app.delete("/delete_startswith", tags=["DELETE"])
def delete_startswith(key: str):
    keys = r.keys(f"{key}*")
    if not keys:
        return {"message": f"No key found that starts with {key}"}
    
    for key in keys:
        r.delete(key)
        
    return {"message": "Records deleted successfully"}
