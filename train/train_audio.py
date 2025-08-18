import os, glob
import numpy as np
import librosa
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

def features_from_wav(path, sr_target=16000):
    y, sr = librosa.load(path, sr=sr_target, mono=True)
    if len(y) < sr:  # pad very short clips
        y = np.pad(y, (0, sr - len(y)))
    # Frame-level features
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    roll = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
    flat = librosa.feature.spectral_flatness(y=y)[0]
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    def stats(v):
        return [np.mean(v), np.std(v)]

    feat = []
    for vec in [zcr, cent, roll, bw, flat]:
        feat += stats(vec)
    # MFCC stats
    for i in range(mfcc.shape[0]):
        feat += stats(mfcc[i])

    return np.array(feat, dtype=np.float32)

def load_data(dir_root='data/audio'):
    """
    Expect:
      data/audio/genuine/*.wav
      data/audio/spoof/*.wav
    """
    X, y = [], []
    for label_name, label in [('genuine',0), ('spoof',1)]:
        for p in glob.glob(os.path.join(dir_root, label_name, '*.wav')):
            try:
                X.append(features_from_wav(p))
                y.append(label)
            except Exception as e:
                print('skip', p, e)
    X = np.stack(X)
    y = np.array(y)
    return X, y

def main():
    X, y = load_data()
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, stratify=y, test_size=0.5, random_state=42)
    clf = RandomForestClassifier(n_estimators=250, random_state=42, class_weight='balanced')
    clf.fit(X_tr, y_tr)
    y_pr = clf.predict(X_te)
    y_pb = clf.predict_proba(X_te)[:,1]
    print(classification_report(y_te, y_pr, digits=4))
    joblib.dump(clf, 'models/audio_clf.joblib')
    print('Saved models/audio_clf.joblib')

if __name__ == "__main__":
    main()
