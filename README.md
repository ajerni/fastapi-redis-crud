# FastAPI CRUD boilerplate for Redis Database

## How to Use

1. Git Clone: `git clone https://github.com/ajerni/fastapi-redis-crud.git`
2. `cd fastapi-redis-crud`
3. Create Virtual Environment: `python -m venv env`
4. Activate Virtual Environment: `source env/bin/activate`
5. Install Dependencies: `pip install -r requirements.txt`
6. `echo "redis_key=xyz" > .env` (replace xyz with your database password)
7. Run Application: `uvicorn main:app --reload`

## Live Demo

- requirements.txt created from `pip freeze` before deployment to Vercel: <https://fastapi-redis-crud.vercel.app/>
- Deployed to production. Run `vercel --prod` to overwrite later.
