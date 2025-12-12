import json
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pydantic import BaseModel

load_dotenv()

app = FastAPI(
    title="MoneyWatcher API",
    version="1.0.0",
    description="API for ingesting Krungthai NEXT notificaition via Macrodroid webhook.",
)


class Payload(BaseModel):
    raw_message: str
    timestamps: datetime


@app.post("/api/test")
async def getparam(body: Request):
    raw_body = await body.body()
    body_str = raw_body.decode("utf-8")

    try:
        # 3. แปลงเป็น JSON แบบไม่เคร่ง (strict=False ยอมให้มี Newline/Control chars ได้)
        body_json = json.loads(body_str, strict=False)
    except json.JSONDecodeError:
        # กันเหนียว: ถ้ายังพังอยู่ ให้ลบตัวอักษรแปลกปลอมออกแบบบ้านๆ เลย
        import re

        # ลบ Control characters (ASCII 0-31) ยกเว้น \n \r \t
        clean_str = re.sub(r"[\x00-\x09\x0b-\x1f]", "", body_str)
        body_json = json.loads(clean_str, strict=False)

    print(f"Data: {body_json}")  # ลอง print ดูผลลัพธ์
