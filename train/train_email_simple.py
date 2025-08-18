import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import joblib

def load_df(path='data/emails_train.csv'):
    # Expect columns: text,label  (label: 1=phish, 0=legit)
    df = pd.read_csv(path)
    assert {'text','label'}.issubset(df.columns)
    return df

def main():
    df = load_df()
    X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], stratify=df['label'],
                                                        test_size=0.2, random_state=42)
    
    # Simple TF-IDF + Logistic Regression (no complex feature engineering for demo)
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1,2), min_df=1, max_features=5000)),
        ('clf', LogisticRegression(max_iter=200))
    ])

    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    print(classification_report(y_test, preds, digits=4))

    joblib.dump(pipeline, 'models/email_clf.joblib')
    print('Saved models/email_clf.joblib')

if __name__ == "__main__":
    main()
