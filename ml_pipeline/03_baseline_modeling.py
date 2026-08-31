import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('outputs/df.csv')

user_baseline = df.groupby('user_id').agg({
    'hour': ['mean', 'std'],
    'session_duration': ['mean', 'std'],
    'data_transfer_mb': ['mean', 'std'],
    'geo_distance_km': ['mean', 'std']
}).reset_index()

user_baseline.columns = ['user_id', 'hour_mean', 'hour_std', 'session_mean', 'session_std',
                         'transfer_mean', 'transfer_std', 'geo_mean', 'geo_std']

user_baseline = user_baseline.fillna(0)

print(f"✓ Baseline created for {len(user_baseline)} users")
print("✓ Each user has: normal hour, session duration, transfer size, geo distance")
print(user_baseline.head(5))

df.to_csv('outputs/df.csv', index=False)
