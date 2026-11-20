
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("dataset/spam_emails.csv")

# Set visualization style
sns.set_style("whitegrid")

# --------------------------------
# 1. Dataset overview
# --------------------------------

print("\nDataset Overview:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

# --------------------------------
# 2. Spam and Ham distribution
# --------------------------------

print("\nEmail Category Distribution:")
print(df["label"].value_counts())

print("\nEmail Category Percentage:")
print(df["label"].value_counts(normalize=True) * 100)

plt.figure(figsize=(7, 5))

sns.countplot(data=df, x="label")

plt.title("Spam vs Ham Email Distribution")
plt.xlabel("Email Category")
plt.ylabel("Number of Emails")

plt.savefig("dataset/email_distribution.png")
plt.show()

# --------------------------------
# 3. Duplicate records
# --------------------------------

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nDuplicate Email Text:")
print(df["text"].duplicated().sum())

# --------------------------------
# 4. Email length analysis
# --------------------------------

df["email_length"] = df["text"].astype(str).apply(len)

print("\nEmail Length Statistics:")
print(df["email_length"].describe())

plt.figure(figsize=(8, 5))

sns.histplot(
    data=df,
    x="email_length",
    hue="label",
    bins=50,
    kde=True
)

plt.title("Email Length Distribution")
plt.xlabel("Email Length (Characters)")
plt.ylabel("Frequency")

plt.savefig("dataset/email_length.png")
plt.show()

# --------------------------------
# 5. Spam vs Ham email length
# --------------------------------

print("\nAverage Email Length by Category:")
print(df.groupby("label")["email_length"].mean())

print("\nEDA Completed Successfully!")


# Improved email length visualization

# Calculate 99th percentile
length_limit = df["email_length"].quantile(0.99)

# Filter only for visualization
plot_df = df[df["email_length"] <= length_limit]

plt.figure(figsize=(10, 6))

sns.histplot(
    data=plot_df,
    x="email_length",
    hue="label",
    bins=50,
    kde=True
)

plt.title("Email Length Distribution (99th Percentile)")
plt.xlabel("Email Length")
plt.ylabel("Frequency")

plt.tight_layout()
plt.savefig("dataset/email_length_improved.png")
plt.show()

print("\n99th percentile email length:", length_limit)

