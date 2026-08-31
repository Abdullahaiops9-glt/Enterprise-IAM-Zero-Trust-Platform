import pandas as pd
import numpy as np
import datetime

# Joiner/Mover/Leaver simulation
users_governance = pd.DataFrame({
    'user_id': ['user_0001', 'user_0002', 'user_0003', 'user_0004', 'user_0005'],
    'status': ['active', 'active', 'terminated', 'active', 'active'],
    'role': ['admin', 'developer', 'analyst', 'admin', 'developer'],
    'department': ['IT', 'Dev', 'Finance', 'IT', 'Dev'],
    'last_access': ['2026-06-20', '2026-06-21', '2026-05-01', '2026-06-21', '2026-06-20']
})

# SoD Rules: Conflicting roles cannot be assigned together
sod_rules = [
    ('admin', 'auditor'),      # Admin cannot be auditor
    ('developer', 'deployer'), # Developer cannot deploy to prod
    ('finance', 'purchaser')    # Finance cannot approve purchases
]

def check_sod(user_roles):
    """Check Segregation of Duties violations"""
    violations = []
    for r1, r2 in sod_rules:
        if r1 in user_roles and r2 in user_roles:
            violations.append(f"SoD Violation: {r1} + {r2}")
    return violations

# Apply SoD check
users_governance['sod_violations'] = users_governance['role'].apply(lambda x: check_sod([x]))

# Auto-disable terminated users
users_governance['auto_action'] = users_governance['status'].apply(
    lambda x: 'DISABLED — Account terminated' if x == 'terminated' else 'ACTIVE'
)

print("✓ Governance engine simulated")
print("\n--- User Lifecycle Status ---")
print(users_governance.to_string())

print("\n--- SoD Rules Active ---")
for r1, r2 in sod_rules:
    print(f"  • {r1.upper()} cannot coexist with {r2.upper()}")
