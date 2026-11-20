
import joblib

from preprocess import clean_text

# 1. Load trained model
model = joblib.load("models/best_spam_model.pkl")

# 2. Load TF-IDF vectorizer
data = joblib.load("models/tfidf_features.pkl")
tfidf = data["vectorizer"]


def predict_email(email):

    # Clean email
    cleaned_email = clean_text(email)

    # Convert email into TF-IDF features
    email_vector = tfidf.transform([cleaned_email])

    # Predict email category
    prediction = model.predict(email_vector)[0]

    # Display result
    if prediction == 1:
        result = "SPAM"
    else:
        result = "HAM (Not Spam)"

    return result


# 3. Test with sample emails
if __name__ == "__main__":

    test_emails = [
        """
        Congratulations! You won a free prize.
        Click here to claim your reward immediately.
        """,

        """
        Hi John, please find the meeting schedule
        attached. Let me know if you have questions.
        """,

        """
        Limited offer! Get 90% discount today.
        Buy now before this offer expires.
        """
    ]

    for i, email in enumerate(test_emails, 1):

        print("\nEmail", i)
        print("Message:", email)

        result = predict_email(email)

        print("Prediction:", result)
        print("-" * 50)
