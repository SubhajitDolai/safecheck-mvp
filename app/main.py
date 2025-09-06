from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from .email_model_simple import score_email
from .audio_model import score_audio_from_file
from .fusion import fuse
from .eml_parser import EMLParser
import tempfile, os

app = FastAPI(title="Safecheck MVP", version="0.1.0")

# Initialize EML parser
eml_parser = EMLParser()

class EmailIn(BaseModel):
    text: str

@app.post("/check_email")
def check_email(payload: EmailIn):
    out = score_email(payload.text)
    return {"channel": "email", **out}

@app.post("/check_eml")
async def check_eml(file: UploadFile = File(...)):
    """Enhanced email analysis using .eml files with complete parsing"""
    try:
        # Read the uploaded .eml file
        eml_content = await file.read()
        eml_text = eml_content.decode('utf-8', errors='ignore')
        
        # Parse the .eml file to extract comprehensive features
        features = eml_parser.extract_features_for_ml(eml_text)
        
        if features is None:
            return {"error": "Failed to parse EML file", "channel": "eml"}
        
        # Use the extracted text for basic classification
        basic_result = score_email(features['text'])
        
        # Add advanced EML-specific analysis
        advanced_features = {
            'link_analysis': {
                'total_links': features['link_count'],
                'suspicious_links': features['suspicious_links'],
                'hidden_links': features['hidden_links']
            },
            'header_analysis': {
                'spf_status': features['spf_record'],
                'sender_suspicious': features['suspicious_sender'],
                'return_path_mismatch': features['return_path_mismatch'],
                'routing_hops': features['received_hops']
            },
            'content_analysis': {
                'has_html': features['has_html'],
                'suspicious_keywords': features['suspicious_keywords'],
                'subject_urgency': features['subject_urgency'],
                'javascript_redirects': features['has_javascript_redirects'],
                'suspicious_css': features['suspicious_css']
            }
        }
        
        # Calculate enhanced risk score
        risk_factors = 0
        
        # Link-based risks
        if features['suspicious_links'] > 0:
            risk_factors += min(features['suspicious_links'] * 0.2, 0.4)
        if features['hidden_links'] > 0:
            risk_factors += min(features['hidden_links'] * 0.15, 0.3)
        
        # Header-based risks
        if features['spf_record'] == 'fail':
            risk_factors += 0.3
        if features['suspicious_sender']:
            risk_factors += 0.2
        if features['return_path_mismatch']:
            risk_factors += 0.25
        
        # Content-based risks
        if features['subject_urgency']:
            risk_factors += 0.2
        if features['has_javascript_redirects']:
            risk_factors += 0.3
        if features['suspicious_css']:
            risk_factors += 0.2
        if features['suspicious_keywords'] > 3:
            risk_factors += 0.2
        
        # Combine basic ML prediction with advanced analysis
        enhanced_prob = min(basic_result['phish_prob'] + risk_factors, 1.0)
        enhanced_label = 1 if enhanced_prob > 0.5 else 0
        
        return {
            "channel": "eml",
            "phish_prob": enhanced_prob,
            "label": enhanced_label,
            "basic_ml_prob": basic_result['phish_prob'],
            "eml_risk_factors": risk_factors,
            "advanced_analysis": advanced_features,
            "file_info": {
                "filename": file.filename,
                "size": len(eml_content),
                "parsed_successfully": True
            }
        }
        
    except Exception as e:
        return {
            "error": f"Failed to process EML file: {str(e)}",
            "channel": "eml",
            "file_info": {
                "filename": file.filename if file else "unknown",
                "parsed_successfully": False
            }
        }

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
