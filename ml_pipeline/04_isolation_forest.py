import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('outputs/df.csv')

# Features for Isolation Forest
iso_features = ['hour_risk', 'geo_risk', 'device_risk', 'ip_risk', 'session_risk', 'transfer_risk', 'behavior_score']

# Train Isolation Forest
iso_model = IsolationForest(
    n_estimators=100,      # Number of trees
    contamination=0.05,   # Expected anomaly ratio (5%)
    random_state=42,
    max_samples=256       # Subsample for efficiency
)

iso_model.fit(df[iso_features])

# Predict: -1 = anomaly, 1 = normal
df['iso_prediction'] = iso_model.predict(df[iso_features])
df['iso_score'] = iso_model.decision_function(df[iso_features])  # Anomaly score (lower = more anomalous)

# Convert to binary: 1 = anomaly, 0 = normal
df['iso_anomaly'] = (df['iso_prediction'] == -1).astype(int)

print("✓ Isolation Forest trained")
print(f"✓ Anomalies detected: {df['iso_anomaly'].sum()} ({df['iso_anomaly'].mean()*100:.1f}%)")
print(f"✓ True anomalies caught: {df[(df['iso_anomaly']==1) & (df['is_anomaly']==1)].shape[0]} of {df['is_anomaly'].sum()}")

# Visualization
plt.figure(figsize=(10, 5))
plt.hist(df[df['is_anomaly']==0]['iso_score'], bins=50, alpha=0.6, label='Normal', color='green')
plt.hist(df[df['is_anomaly']==1]['iso_score'], bins=50, alpha=0.6, label='Anomaly', color='red')
plt.axvline(x=iso_model.offset_, color='yellow', linestyle='--', label='Threshold')
plt.xlabel('Isolation Forest Score (lower = more anomalous)')
plt.ylabel('Count')
plt.title('Isolation Forest: Anomaly Score Distribution')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('outputs/isolation_forest.png', dpi=150, bbox_inches='tight')
plt.show()
df.to_csv('outputs/df.csv', index=False)

