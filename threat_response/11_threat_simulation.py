import pandas as pd
import numpy as np

df = pd.read_csv('outputs/df.csv')

def simulate_threat(scenario_name, user_data):
    """Simulate attack and system response"""
    print(f"\n{'='*60}")
    print(f"SCENARIO: {scenario_name}")
    print(f"{'='*60}")

    # Calculate risk
    risk = user_data['risk_score']
    level = user_data['risk_level']

    print(f"User: {user_data['user_id']}")
    print(f"Risk Score: {risk}/100 ({level})")
    print(f"Indicators: Hour={user_data['hour']}, Device={user_data['device_risk']}, "
          f"IP={user_data['ip_risk']}, Transfer={user_data['data_transfer_mb']:.1f}MB")

    # System response
    if level == 'HIGH':
        response = {
            'action': 'ACCESS_DENIED',
            'mfa_triggered': False,
            'account_disabled': True,
            'soc_alert': 'CRITICAL',
            'session_terminated': True,
            'credential_rotated': True,
            'governance_log': 'AUTO_LOGGED'
        }
    elif level == 'MEDIUM':
        response = {
            'action': 'STEP_UP_MFA',
            'mfa_triggered': True,
            'account_disabled': False,
            'soc_alert': 'WARNING',
            'session_terminated': False,
            'credential_rotated': False,
            'governance_log': 'AUTO_LOGGED'
        }
    else:
        response = {
            'action': 'ALLOW',
            'mfa_triggered': False,
            'account_disabled': False,
            'soc_alert': 'NONE',
            'session_terminated': False,
            'credential_rotated': False,
            'governance_log': 'STANDARD'
        }

    print("\n--- Automated Response ---")
    for k, v in response.items():
        print(f"  {k}: {v}")

    return response

# Scenario 1: Stolen credential — odd hour, new device
scenario1 = df[(df['hour'] < 6) & (df['device_risk'] == 2) & (df['is_anomaly'] == 1)].iloc[0]
simulate_threat("Stolen Credential Attack", scenario1)

# Scenario 2: Insider threat — trusted device, massive data transfer
scenario2 = df[(df['data_transfer_mb'] > 500) & (df['is_anomaly'] == 1)].iloc[0]
simulate_threat("Insider Data Exfiltration", scenario2)

# Scenario 3: Account takeover — bad IP, failed logins
scenario3 = df[(df['ip_risk'] == 2) & (df['login_success'] == 0) & (df['is_anomaly'] == 1)].iloc[0]
simulate_threat("Account Takeover", scenario3)

print(f"\n{'='*60}")
print("✓ All 3 threat scenarios simulated with automated response")
print(f"{'='*60}")
