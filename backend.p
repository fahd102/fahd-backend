
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

app = FastAPI()

API_KEY = "monster_secret_123"

# ربط مجلد static ليقدم ملفات الفرونت
app.mount("/static", StaticFiles(directory="static"), name="static")

class ConvertRequest(BaseModel):
    language: str
    code: str

def verify_api_key(authorization: str | None):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    token = authorization[7:]
    if token != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

@app.post("/convert")
async def convert_code(request: ConvertRequest, authorization: str | None = Header(default=None)):
    verify_api_key(authorization)

    language = request.language.lower()
    code = request.code

    filename = f"converted_code.{language}"
    file_path = os.path.join("static", filename)
    os.makedirs("static", exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    return {"download_link": f"/static/{filename}"}

# تعديل نقطة الدخول لعرض صفحة تسجيل الدخول
@app.get("/", response_class=FileResponse)
async def root():
    return FileResponse("static/login.html")

# خدمة ملفات static (اختياري لو ما عرفت تستخدم app.mount بشكل جيد)
@app.get("/static/{file_path:path}")
async def serve_static(file_path: str):
    full_path = os.path.join("static", file_path)
    if os.path.exists(full_path):
        return FileResponse(full_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")

