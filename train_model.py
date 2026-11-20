
import joblib
import pandas as pd

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# 1. Load TF-IDF features
data = joblib.load("models/tfidf_features.pkl")

X_train = data["X_train"]
X_test = data["X_test"]

y_train = data["y_train"]
y_test = data["y_test"]

# 2. Define ML models
models = {
    "Naive Bayes": MultinomialNB(),

    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        random_state=42
    ),

    "Linear SVM": LinearSVC(
        random_state=42
    )
}

results = []

best_model = None
best_f1 = -1
best_model_name = ""

# 3. Train and evaluate each model
for name, model in models.items():

    print("\n" + "=" * 50)
    print("Training:", name)

    # Train model
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)

    precision = precision_score(
        y_test, y_pred, zero_division=0
    )

    recall = recall_score(
        y_test, y_pred, zero_division=0
    )

    f1 = f1_score(
        y_test, y_pred, zero_division=0
    )

    # Display results
    print("\nAccuracy:", round(accuracy * 100, 2), "%")
    print("Precision:", round(precision * 100, 2), "%")
    print("Recall:", round(recall * 100, 2), "%")
    print("F1 Score:", round(f1 * 100, 2), "%")

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1
    })

    # Select model based on F1 score
    if f1 > best_f1:
        best_f1 = f1
        best_model = model
        best_model_name = name

# 4. Compare models
results_df = pd.DataFrame(results)

print("\n" + "=" * 50)
print("MODEL COMPARISON")
print("=" * 50)

print(results_df.to_string(index=False))

# 5. Save the best model
joblib.dump(
    best_model,
    "models/best_spam_model.pkl"
)

print("\nBest Model:", best_model_name)

print("Best F1 Score:", round(best_f1 * 100, 2), "%")

print("\nBest model saved successfully!")
