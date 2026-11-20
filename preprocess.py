
import re
import html


def clean_text(text):
    """
    Clean email text using NLP preprocessing.
    """

    # Convert input into string
    text = str(text)

    # Convert HTML entities
    text = html.unescape(text)

    # Convert text to lowercase
    text = text.lower()

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Replace URLs with a common token
    text = re.sub(
        r"(https?://\S+|www\.\S+)",
        " urltoken ",
        text
    )

    # Replace email addresses
    text = re.sub(
        r"\b[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}\b",
        " emailtoken ",
        text
    )

    # Remove unnecessary special characters
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


# Test preprocessing
if __name__ == "__main__":

    sample_email = """
    Congratulations! You have WON $1000.
    Click https://example.com to claim your prize!
    Contact us at support@example.com
    """

    cleaned_email = clean_text(sample_email)

    print("Original Email:")
    print(sample_email)

    print("\nCleaned Email:")
    print(cleaned_email)

    print("\nPreprocessing completed successfully!")
