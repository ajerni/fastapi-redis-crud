from typing import Any, Dict
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from connections.redis_db import REDIS_CLIENT as r
from frontend.index_html import html
from helper_functions.helpers import getallpairs, getallpairs_starswith, getone
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FastAPI CURD on Redis")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

origins = [
    "http://localhost:5500",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#root route - see frontend
@app.get("/", tags=["Frontend Landing Page"])
async def root():
    return HTMLResponse(html)

### CRUD ###

## CREATE ##

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

@app.get("/read_one", tags=["READ"])
async def read_one(result: dict = Depends(getone)):
    return result

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
