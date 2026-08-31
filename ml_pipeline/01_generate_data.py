import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)
n_samples = 5000

data = {
    'user_id': [f'user_{i:04d}' for i in range(n_samples)],
    'hour': np.random.normal(14, 3, n_samples).astype(int) % 24,
    'day_of_week': np.random.choice([0,1,2,3,4,5,6], n_samples, p=[0.18,0.18,0.18,0.18,0.18,0.05,0.05]),
    'ip_reputation': np.random.choice([0,1,2], n_samples, p=[0.85,0.10,0.05]),
    'device_trust': np.random.choice([0,1,2], n_samples, p=[0.80,0.15,0.05]),
    'login_success': np.random.choice([0,1], n_samples, p=[0.05,0.95]),
    'session_duration': np.random.normal(240, 60, n_samples),
    'data_transfer_mb': np.random.exponential(25, n_samples),
    'geo_distance_km': np.random.exponential(10, n_samples),
}

df = pd.DataFrame(data)

n_anomalies = int(n_samples * 0.05)
anomaly_idx = np.random.choice(df.index, n_anomalies, replace=False)

df.loc[anomaly_idx[:n_anomalies//3], 'hour'] = np.random.choice([2,3,4,5], n_anomalies//3)
df.loc[anomaly_idx[:n_anomalies//3], 'device_trust'] = 2

df.loc[anomaly_idx[n_anomalies//3:2*n_anomalies//3], 'data_transfer_mb'] = np.random.uniform(500, 2000, n_anomalies//3)
df.loc[anomaly_idx[n_anomalies//3:2*n_anomalies//3], 'session_duration'] = np.random.uniform(5, 15, n_anomalies//3)

df.loc[anomaly_idx[2*n_anomalies//3:], 'ip_reputation'] = 2
df.loc[anomaly_idx[2*n_anomalies//3:], 'login_success'] = 0
df.loc[anomaly_idx[2*n_anomalies//3:], 'geo_distance_km'] = np.random.uniform(5000, 15000, n_anomalies - 2*n_anomalies//3)

noise_idx = np.random.choice(df.index, int(n_samples * 0.08), replace=False)
df.loc[noise_idx, 'data_transfer_mb'] += np.random.normal(0, 100, len(noise_idx))
df.loc[noise_idx, 'hour'] = np.random.randint(0, 24, len(noise_idx))
df['data_transfer_mb'] = df['data_transfer_mb'].clip(lower=0.01)
overlap_idx = np.random.choice(df.index, int(n_samples * 0.03), replace=False)
df.loc[overlap_idx, 'data_transfer_mb'] = np.random.uniform(300, 600, len(overlap_idx))

df['is_anomaly'] = 0
df.loc[anomaly_idx, 'is_anomaly'] = 1

flip_idx = np.random.choice(df.index, int(n_samples * 0.02), replace=False)
df.loc[flip_idx, 'is_anomaly'] = 1 - df.loc[flip_idx, 'is_anomaly']

print(f"✓ Dataset created: {n_samples} records, {n_anomalies} anomalies ({n_anomalies/n_samples*100:.1f}%)")
print(f"✓ Normal: {df['is_anomaly'].value_counts()[0]}, Anomalies: {df['is_anomaly'].value_counts()[1]}")
print(df.head(10))

df.to_csv('outputs/df.csv', index=False)
