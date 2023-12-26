# MD5 hash calculation service for files

## Description
This repository contains the solution to a test task. The task was to implement a minimal REST API with a queue and database to save the md5 hash. The API should implement endpoints for uploading a file and accessing the results in the database.

### Stack
- FastAPI
- Redis
- Celery
- PostgreSQL
- SQLAlchemy
- Docker

## Deployment
1. Create `appdata` folder in the project folder. This folder is for the log file.
2. Create a copy of the `env.sample` file and rename it to `.env`.
3. Run docker deployment. You have two options:
    a. `docker-compose -f docker-compose.yml -f docker-compose.devtools.yml up --build` if you need core services and monitoring services (pgadmin and flower). Or:
    b. `docker-compose up --build` if you need just API core services.

#### Add or remove workers
You can configure the required number of workers in the `docker-compose.yml` file:
```
  ...
  celery_worker:
    command: celery -A src.hashing_worker.worker:celery worker --loglevel=INFO
    restart: always
    deploy:
      mode: replicated
      replicas: 2  <-- Specify the required number of workers
  ...
```

## Usage
1. After the build, visit the page <http://127.0.0.1:8000/>.
You should see the main page:
[screen main-page]

2. Select the file and click ***Upload***.
[screen]

3. Copy the file ID.
[screen]

4. Enter the ID of your file in the ***Enter the file ID:*** field .
[screen]
5. Press the ***Get hash*** button.
[screen]
6. You have received the md5 hash of your file.