from email_model import extract_url_features
import pandas as pd
import re
from urllib.parse import urlparse
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report
from sklearn.base import BaseEstimator, TransformerMixin
import joblib

SUS_TLDS = {'.tk', '.ga', '.ml', '.cf', '.gq'}
SUS_TOKENS = ['verify', 'update', 'urgent', 'otp', 'password', 'bank', 'account', 'invoice', 'pay',
              'gift', 'limited', 'click', 'mfa', 'login', 'security', 'suspend']

def extract_urls(txt):
    if not isinstance(txt, str):
        return []
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
        import numpy as np
        return np.array(rows)

def load_df(path='data/emails_train.csv'):
    # Expect columns: text,label  (label: 1=phish, 0=legit)
    df = pd.read_csv(path)
    assert {'text','label'}.issubset(df.columns)
    return df



def main():
    tfidf = TfidfVectorizer(ngram_range=(1,2), min_df=2, max_features=40000)
    url_feats = FunctionTransformer(extract_url_features, validate=False)
    pipeline = Pipeline([
        ('features', FeatureUnion(transformer_list=[
            ('tfidf', tfidf),
            ('url', url_feats),
        ])),
        ('clf', LogisticRegression(max_iter=200, n_jobs=None))
    ])

