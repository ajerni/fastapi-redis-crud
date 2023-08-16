html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI CRUD on Redis and Vercel</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
        
            <h1 id="FastAPI-CRUD-boilerplate-for-Redis-Database">FastAPI CRUD boilerplate for Redis Database</h1>

<h2 id="How-to-Use">How to Use</h2>

<ol>
<li><code>git clone https://github.com/ajerni/fastapi-redis-crud.git</code></li>
<li><code>python -m venv env</code></li>
<li><code>source env/bin/activate</code></li>
<li><code>pip install -r requirements.txt</code></li>
<li><code>uvicorn main:app --reload</code></li>
</ol>

<h2 id="Live-Demo">Live Demo</h2>

<p>Requirements.txt created from <code>pip freeze</code> before deployment to Vercel: <a href="https://fastapi-redis-crud.vercel.app/">fastapi-redis-crud.vercel.app</a>.</p>

<p>Deployed to production. Run <code>vercel --prod</code> to overwrite later.</p>

            <img src="/static/maneblo_logo.png" alt="maneblo" width="200" height="200">
            <ul>
                <li><a href="/docs">/docs</a></li>
                <li><a href="/redoc">/redoc</a></li>
            </ul>
        </div>
    </body>
</html>
"""