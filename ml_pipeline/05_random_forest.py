import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')
df = pd.read_csv('outputs/df.csv')

# Features for Random Forest
rf_features = ['hour_risk', 'geo_risk', 'device_risk', 'ip_risk', 'session_risk', 'transfer_risk',
               'behavior_score', 'failure_streak']

X = df[rf_features]
y = df['is_anomaly']

# Split: 80% train, 20% test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Train Random Forest
rf_model = RandomForestClassifier(
    n_estimators=100,      # Number of trees
    max_depth=10,          # Prevent overfitting
    min_samples_split=5,   # Minimum samples to split node
    class_weight='balanced',  # Handle imbalance (95% normal, 5% anomaly)
    random_state=42
)

rf_model.fit(X_train, y_train)

# Predictions
y_pred = rf_model.predict(X_test)

print("✓ Random Forest trained")
print("\n--- Classification Report ---")
print(classification_report(y_test, y_pred, target_names=['Normal', 'Anomaly']))

# Feature importance
importance = pd.DataFrame({
    'feature': rf_features,
    'importance': rf_model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n--- Feature Importance ---")
print(importance)
import pickle
with open('outputs/rf_model.pkl', 'wb') as f:
    pickle.dump(rf_model, f)
print("✓ Random Forest model saved")

df.to_csv('outputs/df.csv', index=False)

