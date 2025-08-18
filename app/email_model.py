import re
from sklearn.base import BaseEstimator, TransformerMixin
from urllib.parse import urlparse
import numpy as np

# --- Feature extraction for URLs ---
SUS_TLDS = {'.tk', '.ga', '.ml', '.cf', '.gq'}
SUS_TOKENS = ['verify', 'update', 'urgent', 'otp', 'password', 'bank', 'account', 'invoice', 'pay',
              'gift', 'limited', 'click', 'mfa', 'login', 'security', 'suspend']

def extract_urls(txt):
    if not isinstance(txt, str):
        return []
        return re.findall(r'(https?://[^\s]+)', txt, flags=re.I)
        return re.findall(r'(https?://[^\s]+)', txt, flags=re.I)

class URLFeatureExtractor(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None): return self
    def transform(self, X):
        rows = []
        for x in X:
            urls = extract_urls(x or "")
            n_urls = len(urls)
            sus_tld = 0
            sus_token = 0
            for u in urls:
                try:
                    host = urlparse(u).netloc.lower()
                    for tld in SUS_TLDS:
                        if host.endswith(tld):
                            sus_tld += 1
                            break
                    if any(tok in u.lower() for tok in SUS_TOKENS):
                        sus_token += 1
                except:
                    pass
            rows.append([n_urls, sus_tld, sus_token])
        return np.array(rows)

def extract_url_features(x):
    return URLFeatureExtractor().transform(x)
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
