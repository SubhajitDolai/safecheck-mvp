import os, numpy as np, joblib, librosa
from .utils import feature_vector_from_signal

AUDIO_MODEL_PATH = os.getenv('AUDIO_MODEL_PATH', 'models/audio_clf.joblib')
_audio_model = None

def load_audio_model():
    global _audio_model
    if _audio_model is None:
        _audio_model = joblib.load(AUDIO_MODEL_PATH)
    return _audio_model

def score_audio_from_file(path: str):
    model = load_audio_model()
    import librosa
    y, sr = librosa.load(path, sr=16000, mono=True)
    feat = feature_vector_from_signal(y, sr)
    proba = float(model.predict_proba([feat])[0][1])  # spoof probability
    label = int(proba >= 0.5)
    return {'spoof_prob': proba, 'label': label}
