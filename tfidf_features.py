
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

from preprocess import clean_text

# 1. Load cleaned dataset
df = pd.read_csv("dataset/cleaned_spam_emails.csv")

# 2. Select input and output columns
X = df["text"].apply(clean_text)
y = df["label_num"]

# 3. Split dataset into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# 4. Create TF-IDF vectorizer
tfidf = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1, 2),
    min_df=2
)

# 5. Fit only on training data
X_train_tfidf = tfidf.fit_transform(X_train)

# 6. Transform testing data
X_test_tfidf = tfidf.transform(X_test)

# 7. Display results
print("\nTF-IDF FEATURE EXTRACTION RESULTS")

print("\nTraining samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])

print("\nTraining matrix shape:", X_train_tfidf.shape)
print("Testing matrix shape:", X_test_tfidf.shape)

print("\nTotal vocabulary features:", len(tfidf.vocabulary_))

print("\nSample vocabulary:")
print(list(tfidf.vocabulary_.keys())[:20])

# 8. Save extracted features
joblib.dump(
    {
        "vectorizer": tfidf,
        "X_train": X_train_tfidf,
        "X_test": X_test_tfidf,
        "y_train": y_train,
        "y_test": y_test
    },
    "models/tfidf_features.pkl"
)

print("\nTF-IDF features saved successfully!")
