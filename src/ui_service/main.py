from fastapi import FastAPI, Request, UploadFile, File, Depends
from fastapi.templating import Jinja2Templates
from secrets import token_hex
from src import database
from src.config import UPLOADED_FILES_PATH
from src.md5_service.worker import get_md5_hash
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="templates")

database.create_table()


@app.get("/")
def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload_and_queue(file: UploadFile = File(...)):
    file_id = token_hex(10)
    file_path = f"{UPLOADED_FILES_PATH}\{file_id}"

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    database.insert_data(file.filename, file_id)

    task = get_md5_hash.delay(file_path)

    return {"success": True, "file_path": file_path, "file_id": file_id,
            "task_id": task.id, "message": "File uploaded successfully"}


@app.post("/upload-page")
def upload_page(request: Request, file: UploadFile = File(...), result=Depends(upload_and_queue)):
    return templates.TemplateResponse("upload_status.html", {"request": request, "uploading_result": result})


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
