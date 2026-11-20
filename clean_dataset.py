
import pandas as pd

# Load original dataset
df = pd.read_csv("dataset/spam_emails.csv")

print("Original dataset shape:", df.shape)

# 1. Check duplicate email texts
duplicate_texts = df[df.duplicated(subset=["text"], keep=False)]

print("\nTotal duplicate email records:")
print(duplicate_texts.shape[0])

# 2. Check whether duplicate texts have conflicting labels
label_conflicts = (
    df.groupby("text")["label"].nunique()
)

conflicts = label_conflicts[label_conflicts > 1]

print("\nEmail texts with conflicting labels:")
print(len(conflicts))

# 3. Remove duplicate email records
df_clean = df.drop_duplicates(subset=["text"], keep="first").copy()

# 4. Remove empty email messages
df_clean["text"] = df_clean["text"].fillna("").astype(str).str.strip()
df_clean = df_clean[df_clean["text"] != ""]

# 5. Verify the cleaned dataset
print("\nCleaned dataset shape:", df_clean.shape)

print("\nClass distribution after cleaning:")
print(df_clean["label"].value_counts())

print("\nRemaining duplicate emails:")
print(df_clean["text"].duplicated().sum())

# 6. Save cleaned dataset
df_clean.to_csv("dataset/cleaned_spam_emails.csv", index=False)

print("\nCleaned dataset saved successfully!")
