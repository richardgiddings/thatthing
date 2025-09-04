# ThatThing

An API using [FastAPI](https://fastapi.tiangolo.com/) with JWT authentication, setup to deploy to [Render](https://render.com/) when new code pushed to this repository. Some key points:

* There is a requirements.txt that contains the dependencies.
* Uses a Postgres database.
* Uses the python-decouple package to move variables out to .env or environment variables.
* Uses JSON Web Tokens (JWT) for authentication.

More detail to be added on the above once I've built the React frontend...

## Thanks

I'm using the template found [here|](https://render.com/docs/deploy-fastapi) as a base to deploy to Render.