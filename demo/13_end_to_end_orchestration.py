import pandas as pd
import numpy as np

df = pd.read_csv('outputs/df.csv')

def access_decision(risk_score, risk_level):
    if risk_level == 'LOW':
        return {'decision': 'ALLOW', 'action': 'Standard access granted', 'mfa_required': False, 'monitoring': 'Standard'}
    elif risk_level == 'MEDIUM':
        return {'decision': 'STEP_UP_MFA', 'action': 'Additional verification required', 'mfa_required': True, 'monitoring': 'Enhanced'}
    else:
        return {'decision': 'DENY', 'action': 'Access blocked, SOC alert triggered', 'mfa_required': False, 'monitoring': 'SOC Alert Sent'}

def full_iam_orchestration(user_id):
    """Complete IAM decision flow: Auth → Risk → Decision → Action"""
    user = df[df['user_id'] == user_id].iloc[0]

    print(f"\n{'='*60}")
    print(f"IAM ORCHESTRATION DEMO — User: {user_id}")
    print(f"{'='*60}")

    # Step 1: Identity Verification
    print("\n[1] IDENTITY VERIFICATION")
    print(f"    User: {user_id}")
    print(f"    Device Trust: {'Trusted' if user['device_risk']==0 else 'New' if user['device_risk']==1 else 'Untrusted'}")
    print(f"    IP Reputation: {'Clean' if user['ip_risk']==0 else 'Suspicious' if user['ip_risk']==1 else 'Malicious'}")

    # Step 2: Behavioral Risk Scoring
    print("\n[2] BEHAVIORAL RISK SCORING")
    print(f"    Hour: {user['hour']} (Risk: {user['hour_risk']})")
    print(f"    Geo Distance: {user['geo_distance_km']:.1f}km (Risk: {user['geo_risk']})")
    print(f"    Data Transfer: {user['data_transfer_mb']:.1f}MB (Risk: {user['transfer_risk']})")
    print(f"    Behavior Score: {user['behavior_score']:.2f}")

    # Step 3: ML Risk Score
    print("\n[3] ML RISK SCORE")
    print(f"    Isolation Forest: {'Anomaly' if user['iso_anomaly']==1 else 'Normal'}")
    print(f"    Random Forest Probability: {user['rf_proba']:.3f}")
    print(f"    ENSEMBLE RISK SCORE: {user['risk_score']}/100 ({user['risk_level']})")

    # Step 4: Policy Decision
    print("\n[4] POLICY DECISION (PDP)")
    decision = access_decision(user['risk_score'], user['risk_level'])
    print(f"    Decision: {decision['decision']}")
    print(f"    Action: {decision['action']}")
    print(f"    MFA Required: {decision['mfa_required']}")

    # Step 5: Governance Log
    print("\n[5] GOVERNANCE & AUDIT")
    print(f"    Event logged: YES")
    print(f"    SOC Alert: {'SENT' if user['risk_level']=='HIGH' else 'NONE'}")
    print(f"    Session monitoring: {decision['monitoring']}")

    print(f"\n{'='*60}")
    print("ORCHESTRATION COMPLETE")
    print(f"{'='*60}")

    return decision

# Demo with 3 users: normal, medium risk, high risk
normal_user = df[df['risk_level'] == 'LOW'].iloc[0]['user_id']
medium_user = df[df['risk_level'] == 'MEDIUM'].iloc[0]['user_id']
high_user = df[df['risk_level'] == 'HIGH'].iloc[0]['user_id']

full_iam_orchestration(normal_user)
full_iam_orchestration(medium_user)
full_iam_orchestration(high_user)

print("\n" + "="*60)
print("✓ END-TO-END DEMO COMPLETE")
print("✓ Flow: Identity → Risk Scoring → ML Ensemble → Policy → Governance")
print("✓ All 3 risk levels demonstrated: LOW, MEDIUM, HIGH")
print("="*60)
