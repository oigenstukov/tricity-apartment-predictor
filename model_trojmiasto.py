import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import joblib
import os

INPUT_CSV = "data/mieszkania_trojmiasto_clean.csv"
MODEL_PATH = "model_trojmiasto.pkl"
PLOT_PATH = "plots/residuals_plot.png"

# Load data
df = pd.read_csv(INPUT_CSV)


# Features and target
X = df.drop(["price", "link", "title"], axis=1)
y = df["price"]

# Identify categorical and numerical columns
categorical_cols = ["city"]
numerical_cols = [col for col in X.columns if col not in categorical_cols]

# Preprocessing pipeline
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numerical_cols),
    ("cat", OneHotEncoder(drop="first"), categorical_cols)
])

# Model pipeline (RandomForestRegressor as default)
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit model
pipeline.fit(X_train, y_train)

# Predict and evaluate
y_pred = pipeline.predict(X_test)
r2 = r2_score(y_test, y_pred)
print(f"R^2 score: {r2:.4f}")

# Save model
joblib.dump(pipeline, MODEL_PATH)
print(f"Model saved to {MODEL_PATH}")

# Residual plot
residuals = y_test - y_pred
plt.figure(figsize=(8, 5))
plt.scatter(y_pred, residuals, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel("Predicted price")
plt.ylabel("Residuals")
plt.title("Residuals Plot")
os.makedirs("plots", exist_ok=True)
plt.savefig(PLOT_PATH)
plt.close()
print(f"Residuals plot saved to {PLOT_PATH}")
