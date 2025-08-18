import joblib
import os

MODEL_PATH = os.getenv('EMAIL_MODEL_PATH', 'models/email_clf.joblib')
_email_model = None

def load_email_model():
    global _email_model
    if _email_model is None:
        _email_model = joblib.load(MODEL_PATH)
    return _email_model

def score_email(text: str):
    model = load_email_model()
    proba = float(model.predict_proba([text])[0][1])  # phishing probability
    label = int(proba >= 0.5)
    return {'phish_prob': proba, 'label': label}
