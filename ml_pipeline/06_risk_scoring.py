import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')
df = pd.read_csv('outputs/df.csv')

rf_features = ['hour_risk','geo_risk','device_risk','ip_risk','session_risk','transfer_risk','behavior_score','failure_streak']
import pickle
with open('outputs/rf_model.pkl', 'rb') as f:
    rf_model = pickle.load(f)
print("✓ Random Forest model loaded")

# Get Random Forest probability (probability of being anomaly)
df['rf_proba'] = rf_model.predict_proba(df[rf_features])[:, 1]

# Normalize Isolation Forest score to 0-1 range (invert so higher = more anomalous)
df['iso_norm'] = 1 - (df['iso_score'] - df['iso_score'].min()) / (df['iso_score'].max() - df['iso_score'].min())

# Ensemble: 60% Random Forest, 40% Isolation Forest
# Why: RF is supervised (more accurate), IF is unsupervised (catches unknown)
df['risk_score'] = (0.6 * df['rf_proba'] + 0.4 * df['iso_norm']) * 100

# Round to integer
df['risk_score'] = df['risk_score'].round().astype(int)

# Risk levels
def risk_level(score):
    if score <= 30:
        return 'LOW'
    elif score <= 70:
        return 'MEDIUM'
    else:
        return 'HIGH'

df['risk_level'] = df['risk_score'].apply(risk_level)

print("✓ Risk Scoring Engine complete")
print(f"✓ Score range: {df['risk_score'].min()} to {df['risk_score'].max()}")
print("\n--- Risk Level Distribution ---")
print(df['risk_level'].value_counts())

# Sample output
print("\n--- Sample Risk Scores ---")
print(df[['user_id', 'hour', 'data_transfer_mb', 'risk_score', 'risk_level', 'is_anomaly']].head(15))
df.to_csv('outputs/df.csv', index=False)

