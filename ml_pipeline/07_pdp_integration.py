import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')
df = pd.read_csv('outputs/df.csv')

# Logic: Risk score → Policy Engine → Allow / MFA / Deny

def access_decision(risk_score, risk_level):
    """Zero Trust PDP: Risk-based access decision"""
    if risk_level == 'LOW':
        return {
            'decision': 'ALLOW',
            'action': 'Standard access granted',
            'mfa_required': False,
            'monitoring': 'Standard'
        }
    elif risk_level == 'MEDIUM':
        return {
            'decision': 'STEP_UP_MFA',
            'action': 'Additional verification required',
            'mfa_required': True,
            'monitoring': 'Enhanced'
        }
    else:  # HIGH
        return {
            'decision': 'DENY',
            'action': 'Access blocked, SOC alert triggered',
            'mfa_required': False,
            'monitoring': 'SOC Alert Sent'
        }

# Apply PDP to all users
df['access_decision'] = df.apply(lambda row: access_decision(row['risk_score'], row['risk_level']), axis=1)

# Extract decision components
df['decision'] = df['access_decision'].apply(lambda x: x['decision'])
df['mfa_required'] = df['access_decision'].apply(lambda x: x['mfa_required'])

print("✓ Zero Trust PDP integrated")
print("\n--- Access Decision Distribution ---")
print(df['decision'].value_counts())

# Show examples
print("\n--- Decision Examples ---")
sample = df[['user_id', 'risk_score', 'risk_level', 'decision', 'mfa_required', 'is_anomaly']].head(20)
print(sample.to_string())
