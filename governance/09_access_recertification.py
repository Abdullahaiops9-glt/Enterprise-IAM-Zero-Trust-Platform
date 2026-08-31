import pandas as pd
import numpy as np
import datetime

users_governance = pd.DataFrame({
    'user_id': ['user_0001', 'user_0002', 'user_0003', 'user_0004', 'user_0005'],
    'status': ['active', 'active', 'terminated', 'active', 'active'],
    'role': ['admin', 'developer', 'analyst', 'admin', 'developer'],
    'department': ['IT', 'Dev', 'Finance', 'IT', 'Dev'],
    'last_access': ['2026-06-20', '2026-06-21', '2026-05-01', '2026-06-21', '2026-06-20']
})

# Reuse users_governance from CELL 9, add recertification fields
review_date = datetime.date(2026, 6, 21)
users_governance['last_access_date'] = pd.to_datetime(users_governance['last_access'])
users_governance['days_since_access'] = (pd.Timestamp(review_date) - users_governance['last_access_date']).dt.days

def recertification_decision(row):
    if row['status'] == 'terminated':
        return 'REVOKE — account already terminated'
    if row['days_since_access'] > 30:
        return 'FLAG FOR REVIEW — inactive over 30 days'
    if row['role'] == 'admin':
        return 'MANUAL APPROVAL REQUIRED — privileged role'
    return 'AUTO-RECERTIFIED — active, low-risk'

users_governance['recert_decision'] = users_governance.apply(recertification_decision, axis=1)

print("✓ Access Review & Recertification Cycle Simulated")
print(f"  Review date: {review_date}\n")
print(users_governance[['user_id', 'role', 'status', 'days_since_access', 'recert_decision']].to_string(index=False))

# Summary counts
summary = users_governance['recert_decision'].value_counts()
print("\n--- Recertification Summary ---")
for decision, count in summary.items():
    print(f"  • {decision}: {count} user(s)")
