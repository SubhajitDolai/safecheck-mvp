import numpy as np
import librosa

def feature_vector_from_signal(y, sr):
    if len(y) < sr:
        y = np.pad(y, (0, sr - len(y)))
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    cent = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    roll = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
    flat = librosa.feature.spectral_flatness(y=y)[0]
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

    def stats(v): return [np.mean(v), np.std(v)]
    feat = []
    for vec in [zcr, cent, roll, bw, flat]: feat += stats(vec)
    for i in range(mfcc.shape[0]): feat += stats(mfcc[i])
    return np.array(feat, dtype=np.float32)
