
from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

app = FastAPI()

# المفتاح السري
API_KEY = "monster_secret_123"

# ربط مجلد static لتقديم الملفات الثابتة (الفرونت إند)
app.mount("/static", StaticFiles(directory="static"), name="static")

# موديل الطلب
class ConvertRequest(BaseModel):
    language: str
    code: str

# تحقق من المفتاح في الهيدر
def verify_api_key(authorization: str | None):
    if authorization is None:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    token = authorization[7:]
    if token != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")

# نقطة تحويل الكود
@app.post("/convert")
async def convert_code(request: ConvertRequest, authorization: str | None = Header(default=None)):
    verify_api_key(authorization)

    language = request.language.lower()
    code = request.code

    # حفظ الكود في ملف داخل static
    filename = f"converted_code.{language}"
    os.makedirs("static", exist_ok=True)
    file_path = os.path.join("static", filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    return {"download_link": f"/static/{filename}"}

# نقطة البداية
@app.get("/")
async def root():
    return {"message": "API is running"}

# تقديم الملفات الثابتة من /static
@app.get("/static/{file_path:path}")
async def serve_static(file_path: str):
    full_path = os.path.join("static", file_path)
    if os.path.exists(full_path):
        return FileResponse(full_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")



from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

