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

### API endpoints

#### Upload file (POST)

Request URL: http://.../upload

Curl: 
```curl
curl -X 'POST' \
  'http://127.0.0.1:8000/upload' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@testfile.txt;type=text/plain'
```

Response:
```json
{
  "success": true,
  "file_id": "cf1f2258f062d5b0dfd7",
  "message": "File uploaded successfully"
}
```

#### Get hash by File ID (GET)

***Option 1:***
Request URL: http://.../result/cf1f2258f062d5b0dfd7

Curl:
```
curl -X 'GET' \
  'http://127.0.0.1:8000/result/cf1f2258f062d5b0dfd7' \
  -H 'accept: application/json'
```
***Option 2:***
Request URL: http://.../result?file_id=cf1f2258f062d5b0dfd7

Curl:
```
curl -X 'GET' \
  'http://127.0.0.1:8000/result?file_id=cf1f2258f062d5b0dfd7' \
  -H 'accept: application/json'
```
Response (success):
```json
{
  "status": "SUCCESS",
  "md5_hash": "05a671c66aefea124cc08b76ea6d30bb"
}
```
Response (pending):
```json
{
  "status": "PENDING",
  "md5_hash": null
}
```


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

 ![scr1](https://github.com/probodis/BG_md5_service/assets/22256398/759e31f2-56e5-4ad5-9cfc-cace31395037)

2. Select the file and click ***Upload***.
   
 ![scr2_1](https://github.com/probodis/BG_md5_service/assets/22256398/581a4cb1-721b-4f86-9674-6c54a4e48555)


3. Copy the file ID.
   
 ![scr3_1](https://github.com/probodis/BG_md5_service/assets/22256398/c7a727f9-1ec2-4f4d-8dab-5fa766b46a9e)


4. Enter the ID of your file in the ***Enter the file ID:*** field.
   
 ![scr4_1](https://github.com/probodis/BG_md5_service/assets/22256398/fcb0cb10-4cf2-444e-a74e-06c488325e37)

5. Press the ***Get hash*** button.

6. You have received the md5 hash of your file.
  
 ![scr5_1](https://github.com/probodis/BG_md5_service/assets/22256398/a469aee7-dceb-4008-9330-b4bc8d01fd82)
    
#### Swagger UI
You can also use the page http://127.0.0.1:8000/docs for endpoints research.
 ![Снимок](https://github.com/probodis/BG_md5_service/assets/22256398/914511ba-5d28-424e-8aee-431c81b3d534)

