# ------------------------------
# 1. Import Libraries
# ------------------------------
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
import joblib

# ------------------------------
# 2. Load Dataset
# ------------------------------
df = pd.read_csv("EW-MAX.csv")

# Convert date to datetime (not used as feature)
df["Date"] = pd.to_datetime(df["Date"])

# ------------------------------
# 3. Create Target (Next-Day Trend)
# ------------------------------
df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

# Remove last row because target will be NaN
df = df[:-1]

# ------------------------------
# 4. Select Features
# ------------------------------
features = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]
X = df[features]
y = df["Target"]

# ------------------------------
# 5. Train/Test Split
# ------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# ------------------------------
# 6. Scaling
# ------------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# ------------------------------
# 7. Train Multiple Models
# ------------------------------

models = {
    "SVM": SVC(kernel="rbf"),
    "RandomForest": RandomForestClassifier(n_estimators=200),
    "GradientBoosting": GradientBoostingClassifier(),
    "LogisticRegression": LogisticRegression(max_iter=2000)
}

accuracies = {}

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    pred = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, pred)
    accuracies[name] = acc
    print(f"{name} Accuracy: {acc:.4f}")

# ------------------------------
# 8. Choose Best Model
# ------------------------------
best_model_name = max(accuracies, key=accuracies.get)
best_model = models[best_model_name]

print("\nBest Model =", best_model_name, "with Accuracy =", accuracies[best_model_name])

# ------------------------------
# 9. Save Best Model + Scaler
# ------------------------------
joblib.dump(best_model, "best_stock_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("\nModel saved successfully!")

