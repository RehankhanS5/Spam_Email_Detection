import os
import requests
from dotenv import load_dotenv
import csv
import re
from io import StringIO

import joblib

from email_validator import (
    validate_email,
    EmailNotValidError
)

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    make_response
)

from preprocess import clean_text
from database import create_table, get_connection

load_dotenv()

SENDER_REGISTRY_API_KEY = os.getenv(
    "SENDER_REGISTRY_API_KEY"
)

SENDER_REGISTRY_URL = (
    "https://www.senderregistry.com/api/v1/check/email"
)


app = Flask(__name__)

# Create database table
create_table()

# Load trained ML model
model = joblib.load("models/best_spam_model.pkl")

# Load TF-IDF vectorizer
data = joblib.load("models/tfidf_features.pkl")
tfidf = data["vectorizer"]


# Save analysis result into database
def save_prediction(email, prediction, analysis_type="MESSAGE"):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO predictions
        (email_preview, prediction, analysis_type)
        VALUES (?, ?, ?)
    """, (email[:150], prediction, analysis_type))

    connection.commit()
    connection.close()


# Check whether input contains only an email address
def is_email_address_only(text):

    email_pattern = r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}"

    return bool(re.fullmatch(email_pattern, text.strip()))


# Check email address and domain
def check_email_address(email):

    try:

        result = validate_email(
            email,
            check_deliverability=True
        )

        return {
            "status": "VALID",
            "title": "Valid Email Address",
            "message": (
                f"The address format is valid and the domain "
                f"{result.domain} has email-delivery records. "
                "This does not confirm sender identity or reputation."
            )
        }

    except EmailNotValidError as e:

        return {
            "status": "INVALID",
            "title": "Invalid Email Address",
            "message": str(e)
        }

    except Exception:

        return {
            "status": "UNVERIFIED",
            "title": "Unable to Verify Domain",
            "message": (
                "The email format may be valid, but the domain "
                "could not be checked. Please try again later."
            )
        }



def check_email_reputation(email):

    if not SENDER_REGISTRY_API_KEY:
        return {
            "status": "UNVERIFIED",
            "title": "API Key Missing",
            "message": "The reputation API key is not configured."
        }

    try:
        response = requests.get(
            SENDER_REGISTRY_URL,
            params={"email": email},
            headers={
                "Authorization": f"Bearer {SENDER_REGISTRY_API_KEY}"
            },
            timeout=8
        )

        response.raise_for_status()
        data = response.json()

        # Available reputation signals
        disposable = data.get("disposable")

        spoofable_data = data.get("spoofable", {})
        if not isinstance(spoofable_data, dict):
            spoofable_data = {}

        spoofable = spoofable_data.get("spoofable")
        grade = spoofable_data.get("grade")
        spf = spoofable_data.get("spf")
        dmarc = spoofable_data.get("dmarc")

        # Identify checks unavailable on the current API plan
        restricted_checks = [
            name for name in (
                "role_account",
                "risky_tld",
                "bulk_sender",
                "known_malicious",
                "mx",
                "domain_reputation"
            )
            if isinstance(data.get(name), dict)
            and data[name].get("upgrade_required") is True
        ]

        signals = {
            "disposable": disposable,
            "spoofable": spoofable,
            "grade": grade,
            "spf": spf,
            "dmarc": dmarc,
            "restricted_checks": restricted_checks
        }

        if disposable is True:
            status = "SUSPICIOUS"
            title = "Disposable Email Address"
            message = (
                "This address appears to use a disposable email service. "
                "This is a risk signal, not proof of malicious activity."
            )

        elif spoofable is True:
            status = "REVIEW_REQUIRED"
            title = "Email Domain Requires Review"
            message = (
                "The domain has a spoofability warning. "
                "Review its SPF and DMARC information. "
                "This does not prove that the sender is spam."
            )

        elif restricted_checks or disposable is None or spoofable is None:
            status = "LIMITED"
            title = "Limited Reputation Check"
            message = (
                "Some reputation checks are unavailable or could not "
                "be completed. No safety conclusion can be made."
            )

        else:
            status = "NO_KNOWN_RISK"
            title = "No Known Reputation Risk"
            message = (
                "No risk signals were found in the available checks. "
                "This does not guarantee that the sender is safe."
            )

        return {
            "status": status,
            "title": title,
            "message": message,
            "signals": signals
        }

    except requests.RequestException as error:
        return {
            "status": "UNVERIFIED",
            "title": "Reputation Check Unavailable",
            "message": (
                "Could not connect to the reputation service. "
                "Please try again later."
            )
        }

    except (ValueError, TypeError):
        return {
            "status": "UNVERIFIED",
            "title": "Invalid API Response",
            "message": (
                "The reputation service returned an unreadable response."
            )
        }


# Home page
@app.route("/", methods=["GET", "POST"])
def home():

    prediction = None
    email_text = ""
    error = None
    address_result = None

    if request.method == "POST":

        analysis_type = request.form.get(
            "analysis_type", "message"
        )

        # EMAIL ADDRESS CHECKER
        if analysis_type == "address":

            sender_email = request.form.get(
                "sender_email", ""
            ).strip()

            if not sender_email:

                error = "Please enter an email address."

            elif len(sender_email) > 254:

                error = "Email address is too long."

            else:

                address_result = check_email_address(
                    sender_email
                )

                # Save address check
                save_prediction(
                    sender_email,
                    address_result["status"],
                    "ADDRESS"
                )

        # EMAIL MESSAGE CHECKER
        elif analysis_type == "message":

            email_text = request.form.get(
                "email", ""
            ).strip()

            if not email_text:

                error = "Please enter an email message."

            elif len(email_text) > 20000:

                error = "Email is too long. Maximum 20,000 characters."

            elif is_email_address_only(email_text):

                error = (
                    "Please enter the email message, "
                    "not just an email address."
                )

            else:

                cleaned_email = clean_text(email_text)

                if not cleaned_email.strip():

                    error = (
                        "Please enter a valid email message "
                        "containing text."
                    )

                else:

                    email_vector = tfidf.transform(
                        [cleaned_email]
                    )

                    result = model.predict(email_vector)[0]

                    prediction = (
                        "SPAM" if result == 1 else "HAM"
                    )

                    # Save message prediction
                    save_prediction(
                        email_text,
                        prediction,
                        "MESSAGE"
                    )

        else:

            error = "Invalid analysis mode selected."

    return render_template(
        "index.html",
        prediction=prediction,
        email_text=email_text,
        error=error,
        address_result=address_result
    )


# Analytics dashboard
@app.route("/dashboard")
def dashboard():

    search = request.args.get(
        "search", ""
    ).strip()

    category = request.args.get(
        "category", "ALL"
    ).upper()

    analysis_type = request.args.get(
        "analysis_type", "ALL"
    ).upper()

    allowed_categories = [
        "ALL", "SPAM", "HAM",
        "VALID", "INVALID", "UNVERIFIED"
    ]

    allowed_types = [
        "ALL", "MESSAGE", "ADDRESS"
    ]

    if category not in allowed_categories:
        category = "ALL"

    if analysis_type not in allowed_types:
        analysis_type = "ALL"

    connection = get_connection()
    cursor = connection.cursor()

    # Total analysis count
    cursor.execute("""
        SELECT COUNT(*) FROM predictions
    """)

    total_emails = cursor.fetchone()[0]

    # Message analysis count
    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE analysis_type = 'MESSAGE'
    """)

    message_count = cursor.fetchone()[0]

    # Address analysis count
    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE analysis_type = 'ADDRESS'
    """)

    address_count = cursor.fetchone()[0]

    # Spam count
    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE analysis_type = 'MESSAGE'
        AND prediction = 'SPAM'
    """)

    spam_count = cursor.fetchone()[0]

    # Ham count
    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE analysis_type = 'MESSAGE'
        AND prediction = 'HAM'
    """)

    ham_count = cursor.fetchone()[0]

    # Address validation counts
    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE analysis_type = 'ADDRESS'
        AND prediction = 'VALID'
    """)

    valid_address_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE analysis_type = 'ADDRESS'
        AND prediction = 'INVALID'
    """)

    invalid_address_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM predictions
        WHERE analysis_type = 'ADDRESS'
        AND prediction = 'UNVERIFIED'
    """)

    unverified_address_count = cursor.fetchone()[0]

    # Build search and filter query
    query = """
        SELECT id, email_preview, prediction,
               created_at, analysis_type
        FROM predictions
        WHERE 1=1
    """

    params = []

    if search:

        query += " AND email_preview LIKE ?"
        params.append(f"%{search}%")

    if category != "ALL":

        query += " AND prediction = ?"
        params.append(category)

    if analysis_type != "ALL":

        query += " AND analysis_type = ?"
        params.append(analysis_type)

    query += " ORDER BY id DESC LIMIT 100"

    cursor.execute(query, params)

    history = cursor.fetchall()

    connection.close()

    return render_template(
        "dashboard.html",
        total_emails=total_emails,
        message_count=message_count,
        address_count=address_count,
        spam_count=spam_count,
        ham_count=ham_count,
        valid_address_count=valid_address_count,
        invalid_address_count=invalid_address_count,
        unverified_address_count=unverified_address_count,
        history=history,
        search=search,
        category=category,
        analysis_type=analysis_type
    )


# Clear prediction history
@app.route("/clear-history", methods=["POST"])
def clear_history():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM predictions")

    connection.commit()
    connection.close()

    return redirect(url_for("dashboard"))


# Export prediction history
@app.route("/export-history")
def export_history():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, email_preview, prediction,
               analysis_type, created_at
        FROM predictions
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    connection.close()

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "Email / Address",
        "Result",
        "Analysis Type",
        "Date"
    ])

    writer.writerows(records)

    response = make_response(
        "\ufeff" + output.getvalue()
    )

    response.headers["Content-Disposition"] = (
        "attachment; filename=mailguard_analysis_history.csv"
    )

    response.headers["Content-Type"] = (
        "text/csv; charset=utf-8"
    )

    return response


# Run Flask application
if __name__ == "__main__":

    app.run(debug=True)
