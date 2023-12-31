from fastapi import FastAPI, Request, UploadFile, File, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from secrets import token_hex
from src.hashing_worker.worker import celery, get_md5_hash, redis_client, redis
from src.config import FILE_EXPIRATION_TIME
import logging
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="src/api_service/templates")

logger = logging.getLogger(__name__)


@app.get("/")
def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
def upload_and_queue(file: UploadFile = File(...)):
    file_id = token_hex(10)

    with file.file as f:
        data = f.read()  # Read the file content as an array of bytes

    try:
        redis_client.set(file_id, data, ex=FILE_EXPIRATION_TIME)

    except redis.RedisError:
        logger.error(f"Error saving a file {file_id} to Redis. Check Redis server.")
        return {"success": False, "file_id": None,
                "message": "File has not been uploaded. Internal error"}

    task = get_md5_hash.apply_async((file_id, file.filename), task_id=file_id)

    return {"success": True, "file_id": file_id,
            "message": "File uploaded successfully"}


@app.post("/upload-page")
def upload_page(request: Request, file: UploadFile = File(...), result=Depends(upload_and_queue)):
    return templates.TemplateResponse("upload_status_page.html", {"request": request, "uploading_result": result})


@app.get("/result")
@app.get("/result/{file_id}")
def get_result_by_id(file_id: str):
    if len(file_id) == 0:
        raise HTTPException(status_code=400, detail="The File ID cannot be empty")
    result = celery.AsyncResult(file_id)
    return {"status": result.status, "md5_hash": result.result}


@app.get("/result-page")
def result_page(request: Request, result=Depends(get_result_by_id)):
    message = result["md5_hash"] if result['status'] == "SUCCESS" else result["status"]
    return templates.TemplateResponse("hashing_result_page.html", {"request": request, "hashing_result": message})


#if __name__ == '__main__':
#    uvicorn.run("main:app", host="127.0.0.1", reload=True)
