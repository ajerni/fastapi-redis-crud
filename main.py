from typing import Any
from fastapi import FastAPI, Depends, HTTPException, status

import redis
import json

from dotenv import load_dotenv
import os

load_dotenv()

r = redis.Redis(
    host="redis-10522.c293.eu-central-1-1.ec2.cloud.redislabs.com",
    port=10522,
    password=os.getenv("redis_key"),
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
r.set("gugus", "guguseli")

print(r.get("blog_key"))

app = FastAPI(title="FastAPI CURD on Redis")

class GetObjectOr404:
    def __init__(self, model) -> None:
        self.model = model

    def __call__(self, id: str):
        obj = self.model.get(id)
        if not obj:
            raise HTTPException(
                detail=f"Object with id {id} does not exist in model {self.model.get('name')}",
                status_code=status.HTTP_404_NOT_FOUND,
            )
        return obj

blog_dependency = GetObjectOr404(blogs)
@app.get("/blog/{id}")
def get_blog(blog_name: str = Depends(blog_dependency)):
    return blog_name

user_dependency = GetObjectOr404(users)
@app.get("/user/{id}")
def get_user(user_name: str = Depends(user_dependency)):
    return user_name