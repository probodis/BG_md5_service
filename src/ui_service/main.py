from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from secrets import token_hex
from src.config import UPLOADED_FILES_PATH
import uvicorn

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/")
def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    file_ext = file.filename.split(".").pop()
    file_name = token_hex(10)
    file_path = f"{UPLOADED_FILES_PATH}\{file_name}.{file_ext}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    return {"success": True, "file_path": file_path, "message": "File uploaded successfully"}


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
