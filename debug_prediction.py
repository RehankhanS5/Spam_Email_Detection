
import joblib

from preprocess import clean_text

# Load trained model
model = joblib.load("models/best_spam_model.pkl")

# Load TF-IDF vectorizer
data = joblib.load("models/tfidf_features.pkl")
tfidf = data["vectorizer"]

# Enter the email you want to test
email = input("Enter your email message: ")

# Clean the email
cleaned_email = clean_text(email)

# Convert into numerical features
email_vector = tfidf.transform([cleaned_email])

# Predict
prediction = model.predict(email_vector)[0]

# Get SVM decision score
score = model.decision_function(email_vector)[0]

print("\n" + "=" * 45)
print("EMAIL ANALYSIS RESULTS")
print("=" * 45)

print("\nOriginal Email:")
print(email)

print("\nCleaned Email:")
print(cleaned_email)

print("\nPrediction:")
print("SPAM" if prediction == 1 else "HAM")

print("\nSVM Decision Score:")
print(round(float(score), 4))

print("\nInterpretation:")

if score > 0:
    print("Model leans toward SPAM")
else:
    print("Model leans toward HAM")

if abs(score) < 0.5:
    print("The score is relatively close to the decision boundary.")
else:
    print("The score is farther from the decision boundary.")

print("\nDebugging completed!")
