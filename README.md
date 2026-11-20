# Spam_Email_Detection
# MailGuard AI – Spam Email Detection

MailGuard AI is a machine learning-based web application designed to identify spam emails and distinguish them from legitimate messages. It also provides email address validation, analysis history, and a dashboard to monitor email checks.

## 🚀 Features

- **Spam Email Detection:** Classifies email messages as Spam or Ham (Legitimate).
- **Machine Learning:** Uses TF-IDF feature extraction and a trained Linear Support Vector Classifier (LinearSVC).
- **Email Address Validation:** Checks email address format and domain deliverability.
- **Interactive Dashboard:** Displays total analyses, spam detections, legitimate messages, and address checks.
- **Analysis History:** Stores previous analysis results using SQLite.
- **Search and Filters:** Filter analysis history by result and analysis type.
- **CSV Export:** Export analysis history for further analysis.
- **User-Friendly Interface:** Built with HTML, CSS, JavaScript, and Flask.

## 🛠️ Technologies Used

**Programming Language**
- Python

**Machine Learning & Data Processing**
- Scikit-learn
- Pandas
- NumPy
- TF-IDF Vectorizer
- LinearSVC

**Backend**
- Flask
- SQLite

**Frontend**
- HTML
- CSS
- JavaScript
- Chart.js

**Other Libraries**
- Joblib
- Requests
- Python-dotenv
- Email-validator

## 📂 Project Structure

```text
Spam_Email_Detection/
│
├── dataset/
│   ├── spam_emails.csv
│   ├── cleaned_spam_emails.csv
│   └── email_distribution.png
│
├── models/
│   ├── tfidf_features.pkl
│   └── best_spam_model.pkl
│
├── templates/
│   ├── index.html
│   └── dashboard.html
│
├── static/
│   ├── style.css
│   └── chart.js
│
├── inspect_dataset.py
├── eda.py
├── clean_dataset.py
├── preprocess.py
├── tfidf_features.py
├── train_model.py
├── predict_email.py
├── database.py
├── app.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/RehankhanS5/Spam_Email_Detection.git
```

### 2. Navigate to the Project Folder

```bash
cd Spam_Email_Detection
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

## 🧠 Machine Learning Workflow

1. Load and inspect the email dataset.
2. Perform exploratory data analysis (EDA).
3. Clean and preprocess email messages.
4. Convert text into numerical features using TF-IDF.
5. Train and evaluate machine learning models.
6. Select the best-performing model.
7. Save the trained model and TF-IDF vectorizer.
8. Use the trained model to predict new email messages.

## 📊 Model Performance

The project evaluates multiple machine learning algorithms and selects the best-performing model based on evaluation metrics.

**Selected Model:** Linear Support Vector Classifier (LinearSVC)

**Test Dataset Results:**
- Accuracy: Approximately 99.04%
- Precision, Recall, and F1-score are evaluated during model testing.

*Note: Performance metrics are based on the project's test dataset and do not guarantee the same performance on all real-world emails.*

## 🖥️ Application Modules

### Email Analysis
Users can enter an email message to identify whether it is spam or legitimate.

### Email Address Validation
Users can enter an email address to check its format and domain deliverability.

### Dashboard
Displays analysis statistics and visual summaries of spam and legitimate messages.

### Analysis History
Stores previous results and provides filtering, searching, and CSV export functionality.

## 🔒 Security

- API keys and environment variables are stored in `.env`.
- Sensitive files are excluded using `.gitignore`.
- Local database files should not be committed to the public repository.

## 🔮 Future Enhancements

- Advanced email sender reputation analysis.
- Integration of additional threat intelligence services.
- Improved phishing email detection.
- Real-time email security monitoring.
- Enhanced model evaluation using additional datasets.

## 👨‍💻 Author

**Pathan Rihan Khan**

B.Tech – Artificial Intelligence and Machine Learning

GitHub: https://github.com/RehankhanS5

---

⭐ If you find this project useful, consider giving the repository a star!
