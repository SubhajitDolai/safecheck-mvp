from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from .email_model_simple import score_email
from .audio_model import score_audio_from_file
from .fusion import fuse
import tempfile, os

app = FastAPI(title="Safecheck MVP", version="0.1.0")

class EmailIn(BaseModel):
    text: str

@app.post("/check_email")
def check_email(payload: EmailIn):
    out = score_email(payload.text)
    return {"channel": "email", **out}

@app.post("/check_audio")
async def check_audio(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    try:
        out = score_audio_from_file(tmp_path)
        return {"channel": "audio", **out}
    finally:
        os.remove(tmp_path)

class FusionIn(BaseModel):
    phish_prob: float | None = None
    spoof_prob: float | None = None
    meta_risk: float | None = 0.0

@app.post("/check_combined")
def check_combined(payload: FusionIn):
    return fuse(payload.phish_prob, payload.spoof_prob, payload.meta_risk or 0.0)

@app.get("/")
def root():
    return {"ok": True, "service": "Safecheck MVP"}
