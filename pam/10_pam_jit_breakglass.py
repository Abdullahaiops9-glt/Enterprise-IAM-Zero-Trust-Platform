import pandas as pd
import numpy as np
import datetime

# Privileged users
pam_users = pd.DataFrame({
    'user_id': ['admin_001', 'admin_002', 'devops_001'],
    'role': ['system_admin', 'security_admin', 'devops_lead'],
    'privilege_level': [3, 3, 2],  # 3 = highest
    'standing_access': [False, False, False],  # JIT only — no standing privileges
    'last_jit_request': ['2026-06-21 10:00', '2026-06-21 14:30', None]
})

def request_jit_access(user_id, reason, duration_minutes=60):
    """Just-In-Time access request simulation"""
    return {
        'user_id': user_id,
        'request_time': '2026-06-21 15:00',
        'approval_status': 'APPROVED',  # In real: workflow approval
        'duration': f'{duration_minutes} minutes',
        'privileges': ['server_reboot', 'config_change', 'log_access'],
        'session_recording': True,
        'credential_vault': 'HashiCorp Vault',
        'auto_revoke': f'2026-06-21 {15 + duration_minutes//60}:{duration_minutes%60:02d}'
    }

# Break-Glass procedure
def break_glass_access(user_id, emergency_reason):
    """Emergency access — bypass normal approval"""
    return {
        'user_id': user_id,
        'type': 'BREAK_GLASS_EMERGENCY',
        'reason': emergency_reason,
        'approval': 'AUTO_APPROVED_WITH_ESCALATION',
        'alert_sent_to': ['soc_team@company.com', 'ciso@company.com'],
        'session_recorded': True,
        'audit_trail': 'FULL_LOG',
        'post_incident_review_required': True,
        'time_limit': '30 minutes'
    }

# Simulate
jit_request = request_jit_access('admin_001', 'Critical server patch', 120)
break_glass = break_glass_access('admin_002', 'Ransomware response — isolate network')

print("✓ PAM + JIT + Break Glass simulated")
print("\n--- JIT Access Request ---")
for k, v in jit_request.items():
    print(f"  {k}: {v}")

print("\n--- Break Glass Emergency Access ---")
for k, v in break_glass.items():
    print(f"  {k}: {v}")
