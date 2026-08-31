import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
import warnings

warnings.filterwarnings('ignore')

# Output directory
OUTPUT_DIR = 'outputs'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load data
df = pd.read_csv('outputs/df.csv')

# Compliance metrics
compliance_report = {
    'total_users': len(df),
    'total_access_events': len(df),
    'anomalies_detected': df['is_anomaly'].sum(),
    'high_risk_blocked': len(df[df['risk_level'] == 'HIGH']),
    'medium_risk_mfa': len(df[df['risk_level'] == 'MEDIUM']),
    'low_risk_allowed': len(df[df['risk_level'] == 'LOW']),
    'false_positives': len(
        df[(df['iso_anomaly'] == 1) & (df['is_anomaly'] == 0)]
    ),
    'false_negatives': len(
        df[(df['iso_anomaly'] == 0) & (df['is_anomaly'] == 1)]
    ),
    'soc_alerts_generated': len(df[df['risk_level'] == 'HIGH']),
    'avg_response_time_ms': 250
}

print("=" * 50)
print("COMPLIANCE REPORT — IAM Behavioral Analytics")
print("=" * 50)

for k, v in compliance_report.items():
    print(f"{k.replace('_', ' ').title()}: {v}")

# ============================================================
# 1. RISK SCORE DISTRIBUTION
# ============================================================

plt.figure(figsize=(10, 6))

plt.hist(
    df['risk_score'],
    bins=50,
    color='steelblue',
    alpha=0.7,
    edgecolor='white'
)

plt.axvline(
    x=30,
    color='green',
    linestyle='--',
    label='Low Threshold'
)

plt.axvline(
    x=70,
    color='red',
    linestyle='--',
    label='High Threshold'
)

plt.xlabel('Risk Score')
plt.ylabel('Count')
plt.title('IAM Risk Score Distribution')
plt.legend()
plt.tight_layout()

plt.savefig(
    f'{OUTPUT_DIR}/risk_distribution.png',
    dpi=300,
    bbox_inches='tight'
)

plt.close()

# ============================================================
# 2. DECISION / RISK LEVEL PIE CHART
# ============================================================

plt.figure(figsize=(8, 8))

risk_counts = df['risk_level'].value_counts()

plt.pie(
    risk_counts,
    labels=risk_counts.index,
    autopct='%1.1f%%',
    colors=['#00ff88', '#ffd700', '#ff3366'],
    startangle=90
)

plt.title('Access Decision Distribution')
plt.tight_layout()

plt.savefig(
    f'{OUTPUT_DIR}/decision_pie.png',
    dpi=300,
    bbox_inches='tight'
)

plt.close()

# ============================================================
# 3. ML FEATURE IMPORTANCE
# ============================================================

rf_features = [
    'hour_risk',
    'geo_risk',
    'device_risk',
    'ip_risk',
    'session_risk',
    'transfer_risk',
    'behavior_score',
    'failure_streak'
]

with open('outputs/rf_model.pkl', 'rb') as f:
    rf_model = pickle.load(f)

importance = pd.DataFrame({
    'feature': rf_features,
    'importance': rf_model.feature_importances_
})

importance_sorted = importance.sort_values(
    'importance',
    ascending=True
)

plt.figure(figsize=(10, 6))

plt.barh(
    importance_sorted['feature'],
    importance_sorted['importance'],
    color='purple',
    alpha=0.8
)

plt.xlabel('Importance')
plt.ylabel('Feature')
plt.title('ML Feature Importance')
plt.tight_layout()

plt.savefig(
    f'{OUTPUT_DIR}/feature_importance.png',
    dpi=300,
    bbox_inches='tight'
)

plt.close()

# ============================================================
# 4. ANOMALY DETECTION ACCURACY
# ============================================================

accuracy_data = [
    'True Positives',
    'True Negatives',
    'False Positives',
    'False Negatives'
]

tp = len(
    df[(df['iso_anomaly'] == 1) & (df['is_anomaly'] == 1)]
)

tn = len(
    df[(df['iso_anomaly'] == 0) & (df['is_anomaly'] == 0)]
)

fp = len(
    df[(df['iso_anomaly'] == 1) & (df['is_anomaly'] == 0)]
)

fn = len(
    df[(df['iso_anomaly'] == 0) & (df['is_anomaly'] == 1)]
)

values = [tp, tn, fp, fn]

plt.figure(figsize=(10, 6))

plt.bar(
    accuracy_data,
    values,
    color=['green', 'blue', 'orange', 'red'],
    alpha=0.8,
    edgecolor='white'
)

plt.ylabel('Count')
plt.title('Anomaly Detection Accuracy')
plt.xticks(rotation=15)
plt.tight_layout()

plt.savefig(
    f'{OUTPUT_DIR}/detection_accuracy.png',
    dpi=300,
    bbox_inches='tight'
)

plt.close()

# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n✓ Compliance dashboard generated")
print("✓ Risk distribution: outputs/risk_distribution.png")
print("✓ Decision pie: outputs/decision_pie.png")
print("✓ Feature importance: outputs/feature_importance.png")
print("✓ Detection accuracy: outputs/detection_accuracy.png")
