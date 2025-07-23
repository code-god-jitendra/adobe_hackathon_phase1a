import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib

# Load CSV
df = pd.read_csv("candidates_without_hindi.csv")

# Feature engineering
df["font_ratio"] = df["font_size"] / df["body_font_size"]

# Select features
features = ["font_size", "is_bold", "x", "y", "char_length", "body_font_size", "font_ratio"]
X = df[features]
y = df["heading"]

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Model
clf = LogisticRegression(max_iter=1000, random_state=42)
clf.fit(X_train, y_train)

# Evaluation
y_pred = clf.predict(X_test)
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save model & scaler
joblib.dump((scaler, clf), "heading_model.pkl", compress=3)
print("✅ Model saved as 'heading_model.pkl'")
