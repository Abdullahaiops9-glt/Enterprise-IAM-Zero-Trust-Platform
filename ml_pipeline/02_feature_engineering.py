import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('outputs/df.csv')

df['hour_risk'] = df['hour'].apply(lambda x: 1 if 9 <= x <= 18 else (2 if 6 <= x <= 22 else 3))

df['geo_risk'] = pd.cut(df['geo_distance_km'], bins=[0, 50, 500, 5000, np.inf], labels=[1,2,3,4]).astype(int)

df['device_risk'] = df['device_trust']

df['ip_risk'] = df['ip_reputation']

df['session_risk'] = pd.cut(df['session_duration'], bins=[0, 30, 120, 480, np.inf], labels=[3,2,1,4]).astype(int)
df['transfer_risk'] = pd.cut(df['data_transfer_mb'], bins=[0, 50, 200, 1000, np.inf], labels=[1,2,3,4]).astype(int)

df['behavior_score'] = (
    df['hour_risk'] * 0.25 +
    df['geo_risk'] * 0.20 +
    df['device_risk'] * 0.20 +
    df['ip_risk'] * 0.15 +
    df['session_risk'] * 0.10 +
    df['transfer_risk'] * 0.10
)

df['failure_streak'] = df['login_success'].apply(lambda x: 1 if x == 0 else 0)

print("✓ Features engineered: hour_risk, geo_risk, device_risk, ip_risk, behavior_score")
print(f"✓ Behavior score range: {df['behavior_score'].min():.2f} to {df['behavior_score'].max():.2f}")
print(df[['user_id', 'hour', 'behavior_score', 'is_anomaly']].head(10))

df.to_csv('outputs/df.csv', index=False)
